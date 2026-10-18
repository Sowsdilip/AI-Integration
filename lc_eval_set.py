# Eval set for letter_of_credit.txt (Day 8, Oct 17 2026)
# key_phrase: text that must appear in a retrieved chunk for a retrieval "hit"
#   (use this instead of chunk_index, since indices change when the chunker changes)
# expected_found=False: the answer is NOT in letter_of_credit.txt.
#   answered_by tells you where it lives if all 4 docs are ingested (None = nowhere).

EVAL_SET = [
    # --- single fact ---
    {"id": "lc-01", "question": "What is a letter of credit?",
     "expected_answer": "A written undertaking by the issuing bank to pay the beneficiary a stated amount if compliant documents are presented.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "written undertaking by a bank"},
    {"id": "lc-02", "question": "Who is the applicant in an LC?",
     "expected_answer": "The buyer (usually the importer) who asks the bank to issue the credit.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "called the applicant"},
    {"id": "lc-03", "question": "Which SWIFT message is used to issue an LC?",
     "expected_answer": "SWIFT MT700.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "MT700"},
    {"id": "lc-04", "question": "Can a beneficiary partially accept an amendment?",
     "expected_answer": "No. Partial acceptance of a single amendment is not allowed (amendments are sent by MT707).",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "Partial acceptance"},
    {"id": "lc-05", "question": "What does a transferable LC allow?",
     "expected_answer": "The first beneficiary (often a middleman) can transfer all or part of the credit to one or more second beneficiaries.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "second beneficiaries"},

    # --- needs reasoning across a paragraph / two chunks ---
    {"id": "lc-06", "question": "What is the difference between an advising bank and a confirming bank?",
     "expected_answer": "The advising bank only authenticates and advises the LC with no payment obligation; the confirming bank adds its own undertaking to pay.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "advising bank"},
    {"id": "lc-07", "question": "How is a sight LC different from a usance LC?",
     "expected_answer": "A sight LC pays as soon as compliant documents are presented; a usance LC pays at a future date, e.g. 90 days after the bill of lading date.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "usance"},
    {"id": "lc-08", "question": "What happens after the seller presents documents to the bank?",
     "expected_answer": "The bank examines them; if compliant it pays and forwards them to the issuing bank, which reimburses it and debits the buyer; the buyer uses the bill of lading to collect the goods.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "examines the documents"},
    {"id": "lc-09", "question": "What are the main risks of an LC for the buyer and the seller?",
     "expected_answer": "Seller: discrepant documents remove the bank's obligation to pay. Buyer: banks deal only in documents, so compliant documents are paid even if the goods are wrong.",
     "expected_found": True, "expected_source": "letter_of_credit.txt", "key_phrase": "discrepant documents"},

    # --- not found in letter_of_credit.txt ---
    {"id": "lc-10", "question": "How many banking days does a bank have to examine documents under UCP 600?",
     "expected_answer": "Not found in letter_of_credit.txt.",
     "expected_found": False, "expected_source": None, "key_phrase": None,
     "answered_by": "ucp600_document_examination.txt"},   # five banking days
    {"id": "lc-11", "question": "What is an 'extend or pay' demand?",
     "expected_answer": "Not found in letter_of_credit.txt.",
     "expected_found": False, "expected_source": None, "key_phrase": None,
     "answered_by": "bank_guarantees.txt"},
    {"id": "lc-12", "question": "What fee does an issuing bank in Dubai charge to open an LC?",
     "expected_answer": "Not found.",
     "expected_found": False, "expected_source": None, "key_phrase": None,
     "answered_by": None},   # near miss: in-domain, but no doc has it
]
