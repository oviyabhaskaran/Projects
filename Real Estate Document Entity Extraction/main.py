
!pip install -q transformers timm easyocr pypdfium2 langchain tiktoken openai chromadb

import cv2
import os
import string
from collections import Counter
from itertools import tee, count
from PIL import Image, ImageEnhance, ImageDraw
from transformers import DetrFeatureExtractor, TableTransformerForObjectDetection
import io
import torch
import asyncio
import easyocr  # Add the EasyOCR library
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from google.colab.patches import cv2_imshow

def PIL_to_cv(pil_img):
  return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def cv_to_PIL(cv_img):
  return Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

easyocr_detector_and_recognizer = easyocr.Reader(['en'], detect_network='craft')
feature_extractor = DetrFeatureExtractor()
table_detector_TATR = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-detection")
table_recognizer_TATR = TableTransformerForObjectDetection.from_pretrained("microsoft/table-transformer-structure-recognition")
table_class = table_recognizer_TATR.config.id2label

def OCR(image):
  result = easyocr_detector_and_recognizer.readtext(image, paragraph=True,
                                                   x_ths=0.2, y_ths=0.2,
                                                   mag_ratio=3, low_text=0.2,
                                                   link_threshold=0.2
                                                   )
  extracted_text = []
  for (_, text) in result:
    extracted_text.append(text)
  return extracted_text

def cell_ocr(img):
  img = PIL_to_cv(img)
  result = easyocr_detector_and_recognizer.readtext(img)
  if result:
    return result[0][1]


def binarizeBlur_image(pil_img):
    image = PIL_to_cv(pil_img)
    thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)[1]
    result = cv2.GaussianBlur(thresh, (5,5), 0)
    result = 255 - result
    return cv_to_PIL(result)

def uniquify(seq, suffs = count(1)):
    """Make all the items unique by adding a suffix (1, 2, etc).
    Credit: https://stackoverflow.com/questions/30650474/python-rename-duplicates-in-list-with-progressive-numbers-without-sorting-list
    `seq` is mutable sequence of strings.
    `suffs` is an optional alternative suffix iterable.
    """
    not_unique = [k for k,v in Counter(seq).items() if v>1]

    suff_gens = dict(zip(not_unique, tee(suffs, len(not_unique))))
    for idx,s in enumerate(seq):
        try:
            suffix = str(next(suff_gens[s]))
        except KeyError:
            continue
        else:
            seq[idx] += suffix
    return seq

class TableExtractionPipeline():

  colors = ["red", "blue", "green", "yellow", "orange", "violet"]

  @staticmethod
  def sharpen_image(pil_img):
      img = PIL_to_cv(pil_img)
      sharpen_kernel = np.array([[-1, -1, -1],
                                  [-1,  9, -1],
                                  [-1, -1, -1]])

      sharpen = cv2.filter2D(img, -1, sharpen_kernel)
      pil_img = cv_to_PIL(sharpen)
      return pil_img


  @staticmethod
  def td_postprocess(pil_img):
      '''
      Removes gray background from tables
      '''
      img = PIL_to_cv(pil_img)

      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
      mask = cv2.inRange(hsv, (0, 0, 100), (255, 5, 255))
      nzmask = cv2.inRange(hsv, (0, 0, 5), (255, 255, 255))
      nzmask = cv2.erode(nzmask, np.ones((3,3))) # (3,3)
      mask = mask & nzmask
      new_img = img.copy()
      new_img[np.where(mask)] = 255
      return cv_to_PIL(new_img)

  def table_detector(self, image, THRESHOLD_PROBA, padd_top, padd_left, padd_bottom, padd_right):
    '''
    Table detection using DEtect-object TRansformer pre-trained on 1 million tables
    '''
    #image = binarizeBlur_image(image)
    image = self.sharpen_image(image)
    #table = self.add_padding(image, padd_top, padd_right, padd_bottom, padd_left)
    encoding = feature_extractor(image, return_tensors="pt")
    with torch.no_grad():
        outputs = table_detector_TATR(**encoding)
    probas = outputs.logits.softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > THRESHOLD_PROBA
    target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
    postprocessed_outputs = feature_extractor.post_process(outputs, target_sizes)
    bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]
    return probas[keep], bboxes_scaled

  def table_struct_recog(self, image, THRESHOLD_PROBA):
    '''
    Table structure recognition using DEtect-object TRansformer pre-trained on 1 million tables
    '''
    encoding = feature_extractor(image, return_tensors="pt")
    with torch.no_grad():
        outputs = table_recognizer_TATR(**encoding)
    probas = outputs.logits.softmax(-1)[0, :, :-1]
    keep = probas.max(-1).values > THRESHOLD_PROBA
    target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
    postprocessed_outputs = feature_extractor.post_process(outputs, target_sizes)
    bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]
    return probas[keep], bboxes_scaled

  def add_padding(self, pil_img, top, right, bottom, left, color=(255,255,255)):
    '''
    Image padding as part of TSR pre-processing to prevent missing table edges
    '''
    width, height = pil_img.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(pil_img.mode, (new_width, new_height), color)
    result.paste(pil_img, (left, top))
    return result

  def crop_tables(self, pil_img, prob, boxes, delta_xmin, delta_ymin, delta_xmax, delta_ymax):
    '''
    crop_tables and plot_results_detection must have same co-ord shifts because 1 only plots the other one updates co-ordinates
    '''
    cropped_img_list = []
    crops = []
    i = 0
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        xmin, ymin, xmax, ymax = xmin-delta_xmin, ymin-delta_ymin, xmax+delta_xmax, ymax+delta_ymax
        cropped_img = pil_img.crop((xmin, ymin, xmax, ymax))
        crops.append((xmin, ymin, xmax, ymax))
        cropped_img_list.append(cropped_img)
        i += 1
    return cropped_img_list, crops

  def generate_structure(self, pil_img, prob, boxes, expand_rowcol_bbox_top, expand_rowcol_bbox_bottom):
    '''
    Co-ordinates are adjusted here by 3 'pixels'
    To plot table pillow image and the TSR bounding boxes on the table
    '''
    rows = {}
    cols = {}
    idx = 0
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        xmin, ymin, xmax, ymax = xmin, ymin, xmax, ymax
        cl = p.argmax()
        class_text = table_class[cl.item()]
        if class_text == 'table row':
            rows['table row.'+str(idx)] = (xmin, ymin-expand_rowcol_bbox_top, xmax, ymax+expand_rowcol_bbox_bottom)
        if class_text == 'table column':
            cols['table column.'+str(idx)] = (xmin, ymin-expand_rowcol_bbox_top, xmax, ymax+expand_rowcol_bbox_bottom)
        idx += 1
    return rows, cols

  def sort_table_featuresv2(self, rows:dict, cols:dict):
    # Sometimes the header and first row overlap, and we need the header bbox not to have first row's bbox inside the headers bbox
    rows_ = {table_feature : (xmin, ymin, xmax, ymax) for table_feature, (xmin, ymin, xmax, ymax) in sorted(rows.items(), key=lambda tup: tup[1][1])}
    cols_ = {table_feature : (xmin, ymin, xmax, ymax) for table_feature, (xmin, ymin, xmax, ymax) in sorted(cols.items(), key=lambda tup: tup[1][0])}
    return rows_, cols_

  def individual_table_featuresv2(self, pil_img, rows:dict, cols:dict):
    for k, v in rows.items():
        xmin, ymin, xmax, ymax = v
        cropped_img = pil_img.crop((xmin, ymin, xmax, ymax))
        rows[k] = xmin, ymin, xmax, ymax, cropped_img
    for k, v in cols.items():
        xmin, ymin, xmax, ymax = v
        cropped_img = pil_img.crop((xmin, ymin, xmax, ymax))
        cols[k] = xmin, ymin, xmax, ymax, cropped_img
    return rows, cols

  def object_to_cells(self, master_row:dict, cols:dict, expand_rowcol_bbox_top, expand_rowcol_bbox_bottom, padd_left):
    '''Removes redundant bbox for rows&columns and divides each row into cells from columns
    Args:
    Returns:

    '''
    cells_img = {}
    header_idx = 0
    row_idx = 0
    previous_xmax_col = 0
    new_cols = {}
    new_master_row = {}
    previous_ymin_row = 0
    new_cols = cols
    new_master_row = master_row

    for k_row, v_row in new_master_row.items():

        _, _, _, _, row_img = v_row
        xmax, ymax = row_img.size
        xa, ya, xb, yb = 0, 0, 0, ymax
        row_img_list = []

        for idx, kv in enumerate(new_cols.items()):
            k_col, v_col = kv
            xmin_col, _, xmax_col, _, col_img = v_col
            xmin_col, xmax_col = xmin_col - padd_left - 10, xmax_col - padd_left

            xa = xmin_col
            xb = xmax_col
            if idx == 0:
                xa = 0
            if idx == len(new_cols)-1:
                xb = xmax
            xa, ya, xb, yb = xa, ya, xb, yb

            row_img_cropped = row_img.crop((xa, ya, xb, yb))
            row_img_list.append(row_img_cropped)

        cells_img[k_row+'.'+str(row_idx)] = row_img_list
        row_idx += 1

    return cells_img, len(new_cols), len(new_master_row)-1

  def pipe_separated_values(self, cell_content, n_cols, n_rows):
    table_data_as_string = ''
    if cell_content:
      for r in range(n_cols, len(cell_content), n_cols):
        if r == n_cols:
          temp = cell_content[0:r]
          temp = [str(t) if t else '' for t in temp]
          if temp:
            table_data_as_string += ('|'.join(temp)) + '\n'
        else:
          temp = cell_content[start:r]
          temp = [str(t) if t else '' for t in temp]
          if temp:
            table_data_as_string += ('|'.join(temp)) + '\n'
        start = r
      return table_data_as_string

  def start_process(self, image, TD_THRESHOLD, TSR_THRESHOLD, padd_top, padd_left, padd_bottom, padd_right, delta_xmin, delta_ymin, delta_xmax, delta_ymax, expand_rowcol_bbox_top, expand_rowcol_bbox_bottom):
    '''
    Initiates the process of generating pandas dataframes from raw pdf-page images
    '''
    final_data = {'table_data': [], 'paragraph_data' : []}
    cropped_content = None
    #Detect and process the table as before
    #image = Image.open(image).convert("RGB")
    cv2_image = PIL_to_cv(image)
    probas, bboxes_scaled_detect = self.table_detector(image, TD_THRESHOLD, padd_top, padd_left, padd_bottom, padd_right)
    if bboxes_scaled_detect.nelement() == 0:
        pass
    else:
      cropped_img_list, cropped_content = self.crop_tables(image, probas, bboxes_scaled_detect, delta_xmin, delta_ymin, delta_xmax, delta_ymax)
      for unpadded_table in cropped_img_list:
        #Hash is the start
        table = binarizeBlur_image(unpadded_table)
        table = self.sharpen_image(table)
        table = self.td_postprocess(unpadded_table)
        table = self.add_padding(unpadded_table, padd_top, padd_right, padd_bottom, padd_left)

        probas, bboxes_scaled = self.table_struct_recog(table, THRESHOLD_PROBA=TSR_THRESHOLD)
        rows, cols = self.generate_structure(table, probas, bboxes_scaled, expand_rowcol_bbox_top, expand_rowcol_bbox_bottom)
        rows, cols = self.sort_table_featuresv2(rows, cols)
        master_row, cols = self.individual_table_featuresv2(table, rows, cols)
        cells_img, max_cols, max_rows = self.object_to_cells(master_row, cols, expand_rowcol_bbox_top, expand_rowcol_bbox_bottom, padd_left)
        sequential_cell_img_list = []
        for k, img_list in cells_img.items():
            for img in img_list:
                sequential_cell_img_list.append(cell_ocr(img))
        table_data_as_string = self.pipe_separated_values(sequential_cell_img_list, max_cols, max_rows)
        final_data['table_data'].append(table_data_as_string)
        #df = self.create_dataframe(sequential_cell_img_list, max_cols, max_rows)
        #json_result = self.create_json(df)
        #final_data['table_data'].append(json_result)
    if cropped_content:
      for hide in cropped_content:
        hide = [int(h) for h in hide]
        cv2.rectangle(cv2_image, (hide[0], hide[1]), (hide[-2], hide[-1]), (255, 255, 255), -1)
    para_content = OCR(cv2_image)
    final_data['paragraph_data'].extend(para_content)
    return final_data

import pypdfium2
from functools import partial

te = TableExtractionPipeline()
ocr_page = partial(te.start_process, TD_THRESHOLD=0.7,
                      TSR_THRESHOLD=0.7,
                      padd_top=50, padd_left=50, padd_bottom=50, padd_right=50,
                      delta_xmin=25, delta_ymin=25, delta_xmax=75,
                      delta_ymax=25, expand_rowcol_bbox_top=0,
                      expand_rowcol_bbox_bottom=0)

#op = ocr_page('/content/test/image_1.jpg')

import warnings
warnings.filterwarnings("ignore")
from tqdm import tqdm

def read_and_ocr_pdf(pdf_path, output_dir):
  content = {}
  pdf = pypdfium2.PdfDocument(pdf_path)
  n_pages = len(pdf)
  for page_number in tqdm(range(n_pages)):
      page = pdf.get_page(page_number)
      pil_image = page.render(scale=200/72).to_pil()
      pil_image.save(f'{output_dir}/image_{page_number}.jpg')
      op = ocr_page(pil_image)
      content[page_number] = op
      with open(f'{output_dir}/page_{page_number}_content.txt', 'w') as f:
        f.write('table:\n')
        for val in op['table_data']:
          f.write(val)
          f.write('\n')
        f.write('\n\n\n')
        for val in op['paragraph_data']:
          f.write(val)
          f.write('\n')
  return content

op = read_and_ocr_pdf('/content/270036.pdf', '/content/test')

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader

import tiktoken  # !pip install tiktoken

tokenizer = tiktoken.get_encoding('p50k_base')
def tiktoken_len(text):
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

from langchain.document_loaders import DirectoryLoader, TextLoader

loader = DirectoryLoader('/content/test', glob="**/*.txt",
                         loader_cls=TextLoader, show_progress=True,
                         use_multithreading=True)

docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 400,
                                               chunk_overlap= 20,
                                               length_function=tiktoken_len,
    separators=["\n\n", "\n", " ", ""])
texts = text_splitter.split_documents(docs)

from langchain.schema import embeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents(documents=texts,
                                    embedding=OpenAIEmbeddings(model='text-embedding-ada-002',
                                    openai_api_key=' ')
                                    )

from langchain.agents import initialize_agent
zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    llm=llm,
    verbose=True,
    max_iterations=3
)

zero_shot_agent("what are the investment highlights?")

zero_shot_agent("write a poem about nature?")
