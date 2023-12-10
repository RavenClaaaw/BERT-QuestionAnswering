from pyPDF2 import PdfReader

def parsepdf(pdf):
    text = ""
    
    reader = PdfReader(pdf)
    for page in reader.pages:
        text += page.extract_text()
    
    with open("context.txt", "w+", encoding='utf-8') as file:
        try:
            file.write(text)
            return main_content.text
        except Exception as error:
            file.write('ERROR PARSING PDF: ' + str(error) + '\n')
                
    return text