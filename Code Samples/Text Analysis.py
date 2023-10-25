class analysedText(object): 
    def __init__ (self, text):
        self.text = text
        l1 = list("!,.:;?`")
        l2 = list(text)
        for j in range(len(text)) :
            for i in range(len(l1)) : 
                if l2[j] == l1[i] : 
                    l2[j] = ' '
                else : 
                    pass
        global fmtext ; fmtext = ''
        for element in l2 :  
            fmtext += element
        fmtext = fmtext.lower().strip()
        return None

    def freqAll(self):
        global base_dict ; base_dict = {}
        word_list = fmtext.split(' ')
        for element in word_list : 
            base_dict[element] = fmtext.count(element)
        base_dict.pop('')
        return base_dict
    
    def freqOf(self, word):
        self.word = word
        base_dict = analysedText(fmtext).freqAll()
        if self.word in base_dict : 
            return base_dict[self.word] 
        else : 
            return "Unfortunantelly, the word you're seeking is not present in the given pattern"

# ------------------------------------------------------------------------------------------------ #

class analysedText(object):
    
    def __init__ (self, text):
        # remove punctuation
        formattedText = text.replace('.','').replace('!','').replace('?','').replace(',','')
        
        # make text lowercase
        formattedText = formattedText.lower()
        
        self.fmtText = formattedText
        
    def freqAll(self):        
        # split text into words
        wordList = self.fmtText.split(' ')
        
        # Create dictionary
        freqMap = {}
        for word in set(wordList): # use set to remove duplicates in list
            freqMap[word] = wordList.count(word)
        
        return freqMap
    
    def freqOf(self,word):
        # get frequency map
        freqDict = self.freqAll()
        
        if word in freqDict:
            return freqDict[word]
        else:
            return 0
    

A = "I love you Karima, you're the one I need in my life !" 

print(analysedText(A).freqOf("karima"))