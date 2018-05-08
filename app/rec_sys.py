from beautifultable import BeautifulTable

import warnings
warnings.filterwarnings("ignore")

doc_info_file = 'data/raw-data.csv'
content_ml_output_file = 'data/content_ml_app_out.dat'
user_collab_ml_output_file = 'data/user_collab_ml_app_output.dat'
autoenco_mf_output_file = 'data/autenco_mf_app_output.dat'
test_file = 'data/ordered-users.dat'

most_rec = 3

def print_meta():
  meta = BeautifulTable()
  meta.column_headers = ["model", "Name"]
  meta.append_row(["COML","Content Based ML Model"])
  meta.append_row(["CUML","Collaborative User Based ML Model"])
  meta.append_row(["CUDL","Collaborative User Based DL Model"])
  meta.append_row(["CDL","Collaborative Deep Learning"])
  print(meta)

print('\n'*3)
table = BeautifulTable()
table.column_headers = ["model", "paperId", "Title", "Present"]
table.column_alignments['Title'] = BeautifulTable.ALIGN_LEFT
table.column_alignments['Present'] = BeautifulTable.ALIGN_RIGHT

# get the content of line from the given file as INTEGERS
def get_line_from_file(file, id):
  i = 0
  docs = []
  f = open(file)
  for line in f:
    docs = line.split()
    if (i == id):
      break
    i += 1
  docs = list(map(int, docs))
  f.close()
  return docs

# read reasearch paper title
def read_doc_info(docId):
  i = 0
  docs = []
  f = open(doc_info_file)
  for line in f:
    docs = line.split(",")
    if (i == docId):
      break
    i += 1
  f.close()
  return docs[3]


# checks if the given docid is present for the given user in test file
def check_in_lib(userId, docId):
  test_docs_for_user = set(get_line_from_file(test_file, userId))
  return  "Yes" if (docId in test_docs_for_user) else "No"


# reads the output of content ML and gets the predicted docs for the given user
def add_content_ml_output(userId):
  docs = get_line_from_file(content_ml_output_file, userId)
  top_rec = docs[:most_rec]
  add_docs_to_result("COML", userId, top_rec)


# reads the output of content ML and gets the predicted docs for the given user
def add_user_collab_ml_output(userId):
  docs = get_line_from_file(user_collab_ml_output_file, userId)
  docs.pop(0) # removing the count
  top_rec = docs[:most_rec]
  add_docs_to_result("CUML", userId, top_rec)

# reads the output of auto enco + mf and gets the predicted docs for the given user
def add_auto__enco_mf_output(userId):
  docs = get_line_from_file(autoenco_mf_output_file, userId)
  docs.pop(0) # removing the count
  top_rec = docs[:most_rec]
  add_docs_to_result("CUDL", userId, top_rec)

def add_docs_to_result(type, userId, recs):
  for r in recs:
    table.append_row([type, r, read_doc_info(r), check_in_lib(userId, r)])


def decoratedRow(str):
  print('-'*50)
  print(str)
  print('-'*50)

def start():
  decoratedRow('Welcome To Recommendation System')
  print_meta()
  validInput = False
  userId  = 0
  while validInput != True:
    userId = input('Enter a userId between {0} - {1} \n'.format(1, 5551))
    userId = int(userId)
    if(userId < 1 or userId > 5551):
      print('Wrong userId')
      validInput = False
    else:
      validInput = True

  print('User ID : {0}'.format(userId))
  userId -=1 # as all IDS are 0 based

  # add content ML output
  add_content_ml_output(userId)

  # add Collab output
  add_user_collab_ml_output(userId)

  # add CDL output

  # add HYBRID output

  # add DEEP COllab output
  add_auto__enco_mf_output(userId)

  print(table)

#####################################################
start()
#####################################################