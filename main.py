import io
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


wnl=WordNetLemmatizer()

def pdf2str(inPDFfile):
    infile = open(inPDFfile,'rb')
    resMgr = PDFResourceManager()
    retData = io.StringIO()
    TxtConverter = TextConverter(resMgr,retData,laparams=LAParams())
    interpreter = PDFPageInterpreter(resMgr,TxtConverter)


    for page in PDFPage.get_pages(infile):
        interpreter.process_page(page)
    txt=retData.getvalue()

    return txt

class Text():
    pdf_text=""
    mat_data=""
    med_data=""
    hist_data=""


#----------  Structure  ---------
    def __init__(self,pdf,matdata,meddata,histdata,choice):
        self.pdf_text=pdf
        self.mat_data=matdata
        self.hist_data=histdata
        self.med_data=meddata


        self.stripPdfText()
        if choice==1:
            self.stripDataText()
        elif choice==2:
            self.striptext()
        self.searchAndClassify()

    def stripPdfText(self):
        self.pdf_text = self.pdf_text.lower()

        symbols = "1234567890!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
        for i in symbols:
            self.pdf_text = self.pdf_text.replace(i, ' ')

        x = ["\u2002", "\x0c", "–", "—", '"', "”"]
        for i in x:
            self.pdf_text = self.pdf_text.replace(i, ' ')

        a=self.pdf_text.split(" ")
        new_text =[]
        for w in a:
            if len(w) > 2:
                new_text.append(wnl.lemmatize(w))
        self.pdf_text=new_text

    def stripDataText(self):
        for i in (self.hist_data, self.med_data, self.mat_data):
            a = i
            a = a.lower()

            symbols = "1234567890!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
            for i in symbols:
                a = a.replace(i, ' ')
            x = ["\u2002", "\x0c", "–", "—", '"', "”"]
            for i in x:
                a = a.replace(i, ' ')
            a = a.replace("’", "")


            new_text = []
            stop_words = set(stopwords.words('english'))

            a = a.split(" ")
            for word in a:
                if word not in stop_words:
                    if len(word) > 2:
                        new_text.append(wnl.lemmatize(word))
            a = new_text
            a = set(a)
            a = list(a)


            if i==self.mat_data:
                self.mat_data=a
            elif i==self.hist_data:
                self.hist_data=a
            elif i==self.med_data:
                self.med_data=a



    def striptext(self):
        matlist=[]
        medlist=[]
        histlist=[]
        for i in self.med_data:
            a=i.replace("\n","")
            medlist.append(a)
        for i in self.mat_data:
            a = i.replace("\n", "")
            matlist.append(a)
        for i in self.hist_data:
            a = i.replace("\n", "")
            histlist.append(a)

        self.mat_data=matlist
        self.med_data=medlist
        self.hist_data=histlist



    def searchAndClassify(self):
        mat_count=0
        med_count=0     #
        hist_count=0

        for i in self.pdf_text:

            if i in self.mat_data and i in self.med_data and i in self.hist_data:
                pass

            else:
                if i in self.mat_data:
                    mat_count+=1
                if i in self.hist_data:
                    hist_count+=1
                if i in self.med_data:
                    med_count+=1

        print("\nOut of the", len(self.pdf_text), "words in selected PDF file")
        print("Medicine:",med_count)
        print("History:",hist_count)
        print("Mathematics:",mat_count)

        print("words were found from the subjects above.")
        if med_count>hist_count and med_count>mat_count:
            print("According to the information above, most of the words are related to medicine with",med_count,"words.")
            print("\nTherefore, the selected PDF is a medical document.")
        elif hist_count>med_count and hist_count>mat_count:
            print("According to the information above, most of the words are related to history with",hist_count,"words.")
            print("\nTherefore, the selected PDF is a historical document.")
        elif mat_count>med_count and mat_count>hist_count:
            print("According to the information above, most of the words are related to mathematics with",mat_count,"words.")
            print("\nTherefore, the selected PDF is a mathematical document.")



#-------------------- main ---------------------
print("The classification process time may vary depending on the number of pages of the selected file.\n")
print("----------- Please Wait -----------")

secim=int(input("Type '1' to classify with cleaned data.\nType '2' to clean test data set.Then start classify(Note:This might increase process time)\n"))

while secim>2 or secim<1:
    secim=int(input("!!!!Something went wrong!!!.\nType '1' to classify with cleaned data.\nType '2' to clean test data set.Then start classify(Note:This might increase process time)\n"))

if secim==2:

    selectedfile=pdf2str('example.pdf')

    history=pdf2str('hist_data.pdf')

    mathematic=pdf2str('math_data.pdf')

    medical=pdf2str('med_data.pdf')

    text=Text(selectedfile,mathematic,medical,history,1)

elif secim==1:
    selectedfile = pdf2str('example3.pdf')
    history=open("hist_data.txt","r")
    mathematic=open("math_data.txt","r")
    medical=open("med_data.txt","r")

    text=Text(selectedfile,mathematic,medical,history,2)







