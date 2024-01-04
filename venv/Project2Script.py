import spacy


def process_email_log(input_file_path, output_file_path, output_file_path_2):
    nlp = spacy.load('en_core_web_sm')

    with open(input_file_path, 'r') as input_file:
        doc = nlp(input_file.read())

    with open(output_file_path, 'w') as parsed_file, open(output_file_path_2, 'w') as parsed_file_2:
        total = 0
        emails = {}

        for token in doc:
            if token.like_email:
                parsed_file.write(f'\nEmail: {token}')

            elif token.tag_ in ('VBG', 'VB'):
                parsed_file.write(f'POS: {token}\n')

            elif token.ent_type != 0:
                parsed_file.write(
                    f'Entity: {token.text} - {token.ent_type_}\n')
        email, org, amount, accAmount = None, None, 0, 0
        for sentence in doc.sents:
            if any(char in sentence.text for char in ('@', '$')):

                for word in sentence:
                    if word.like_email:
                        email, org, amount, accAmount = word, '', 0, 0
                        if email not in emails:
                            emails[email] = {}
                    elif word.pos_ == "SYM":
                        if word.head.text == 'thousand':
                            amount = float(
                                next(w for w in word.head.lefts if w.pos_ == "NUM").text) * 1000
                        else:
                            amount = float(word.head.text.replace(",", ""))
                        accAmount += amount
                        total += amount
                    elif word.ent_type_ == 'ORG' and word.text != 'Inc.':
                        org = word
                        if email is not None:
                            emails[email][org] = amount

        for email, details in emails.items():
            expression = f'{email} :'
            orgs, accumulatedOrgs, accumulatedAmount = [], [], 0

            for org, currentAmount in details.items():
                orgs.append(f'${currentAmount:,.2f} to {org}')
                accumulatedAmount += currentAmount
                accumulatedOrgs.append(str(org))

            entity = ', '.join(accumulatedOrgs[:-1]) + f' and {accumulatedOrgs[-1]}' if len(
                accumulatedOrgs) > 1 else accumulatedOrgs[0]
            expression += f' ${accumulatedAmount:,.2f} to {entity}.'

            for i, (org, currentAmount) in enumerate(details.items()):
                if len(accumulatedOrgs) > 1:
                    if i < len(accumulatedOrgs) - 2:
                        expression += f' ${currentAmount:,.2f} to {org},'
                    elif i == len(accumulatedOrgs) - 2:
                        expression += f' ${currentAmount:,.2f} to {org} and'
                    else:
                        expression += f' ${currentAmount:,.2f} to {org}.'

            print(expression + "\n")
            parsed_file_2.write(expression + "\n")

        print(f"\nTotal Requests: ${total:,.2f}")
        parsed_file_2.write(f"\nTotal Requests: ${total:,.2f}")


input_file_path = "EmailLog.txt"
output_file_path = "parsedText.txt"
output_file_path_2 = "summary_report.txt"
process_email_log(input_file_path, output_file_path, output_file_path_2)
