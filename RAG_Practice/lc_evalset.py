EVAL_SET = [
  # single fact
  {"id":"lc-01","question":"What is a letter of credit?","expected_answer":"A written undertaking by the issuing bank to pay the beneficiary a stated amount if compliant documents are presented.","expected_found":True,"key_phrase":"written undertaking by a bank"},
  {"id":"lc-02","question":"Who is the applicant in an LC?","expected_answer":"The buyer (usually the importer) who asks the bank to issue the credit.","expected_found":True,"key_phrase":"called the applicant"},
  {"id":"lc-03","question":"Which SWIFT message is used to issue an LC?","expected_answer":"SWIFT MT700.","expected_found":True,"key_phrase":"MT700"},
  {"id":"lc-04","question":"Can a beneficiary partially accept an amendment?","expected_answer":"No, partial acceptance of a single amendment is not allowed (amendments go by MT707).","expected_found":True,"key_phrase":"Partial acceptance"},
  {"id":"lc-05","question":"What does a transferable LC allow?","expected_answer":"The first beneficiary (often a middleman) can transfer all or part of the credit to one or more second beneficiaries.","expected_found":True,"key_phrase":"second beneficiaries"},
  # need reasoning across a paragraph or two chunks
  {"id":"lc-06","question":"What is the difference between an advising bank and a confirming bank?","expected_answer":"The advising bank only authenticates and advises, with no payment obligation; the confirming bank adds its own undertaking to pay.","expected_found":True,"key_phrase":"advising bank"},
  {"id":"lc-07","question":"How is a sight LC different from a usance LC?","expected_answer":"Sight pays as soon as compliant documents are presented; usance pays at a future date, e.g. 90 days after the bill of lading date.","expected_found":True,"key_phrase":"usance"},
  {"id":"lc-08","question":"What happens after the seller presents documents to the bank?","expected_answer":"The bank examines them; if compliant it pays and forwards them to the issuing bank, which reimburses it and debits the buyer; the buyer uses the bill of lading to collect the goods.","expected_found":True,"key_phrase":"examines the documents"},
  {"id":"lc-09","question":"What are the main risks of an LC for the buyer and the seller?","expected_answer":"Seller: discrepant documents remove the bank's obligation to pay. Buyer: banks deal only in documents, so compliant documents are paid even if the goods are wrong.","expected_found":True,"key_phrase":"discrepant documents"},
  # not found in letter_of_credit.txt
  {"id":"lc-10","question":"How many banking days does a bank have to examine documents under UCP 600?","expected_answer":"Not found.","expected_found":False,"answered_by":"ucp600_document_examination.txt"},
  {"id":"lc-11","question":"What is an 'extend or pay' demand?","expected_answer":"Not found.","expected_found":False,"answered_by":"bank_guarantees.txt"},
  {"id":"lc-12","question":"What fee does an issuing bank in Dubai charge to open an LC?","expected_answer":"Not found.","expected_found":False,"answered_by":None},
]