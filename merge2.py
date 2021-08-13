class Subtitle:
    def __init__(self, index, time_frame, text):
        self.index = index
        self.start_time = time_frame.split(' ')[0].replace(',', ':')
        self.end_time = time_frame.split('> ')[1].strip().replace(',', ':')
        text = only_letters(text)
        if(type(text)==str):
            self.text = text
        else:
            self.text = ""
            while len(text) > 0:
                self.text += text[0]

class SubSrt:
    def __init__(self, begin_time, end_time, text , person ):
        self.begin_time = begin_time
        self.end_time = end_time
        self.text = text
        self.person = person

    def __add__(self, other):
        if self == None:
            return other
        if self.person == other.person:
            return SubSrt(self.begin_time, other.end_time, self.text.strip() + " " + other.text.strip(), self.person)
        else:
            raise "differ"

    def __str__(self):
        return self.begin_time + ',' + self.end_time + ',' + self.text + ',' + self.person + '\n'

def only_letters(text):
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    ret = ""
    for c in text:
        if allowed_chars.find(c) > -1:
            ret += c
    return ret.lower().strip()
        

def subtitle_to_list(file_name):
    sub_lst = []
    with open(file_name, "r",encoding='UTF-8') as subtitles:
        while True:
            index = subtitles.readline().strip()
            time = subtitles.readline().strip()
            text = subtitles.readline().strip()
            next_line = subtitles.readline()
            if next_line == "\n":
                sub_lst.append(Subtitle(index, time, text))
                continue
            if next_line != "":
                text += " " + next_line.strip()
                sub_lst.append(Subtitle(index, time, text))
                subtitles.readline()
            else:
                return sub_lst

def parse_by_words(name, text, subtitle_list, subtitle_index):
    frame_text = ""
    count = 0
    qs = None
    for word in text.split(' '):
        if subtitle_list[subtitle_index].text.find(word) >-1:
            frame_text += word + " "
        elif subtitle_list[subtitle_index+1].text.find(word) >-1:
            frame:Subtitle = subtitle_list[subtitle_index]
            s  = SubSrt(frame.start_time, frame.end_time, frame_text, name)
            frame_text = word +" "
            if qs == None:
                qs = s
            else:
                qs = qs +s
            count += 1
            subtitle_index += 1
    
    #check if we finished this srt
    if subtitle_list[subtitle_index].text.split(' ')[-1] == word:
        count += 1
    frame:Subtitle = subtitle_list[subtitle_index]
    s  = SubSrt(frame.start_time, frame.end_time, frame_text, name)
    if qs == None:
        qs = s
    else:
        qs = qs +s  
    return qs, count

def main():
    with open("srt-script.csv", "w") as new_script , open("script.txt", "r") as original_script:
        subtitle_list = subtitle_to_list("subtitle.srt")
        subtitle_index = 0
        current_sub = subtitle_list[0]
        script = original_script.readlines()
        for line in script:
            if line.strip()=="":
                continue
            #get name from script, and his text
            name = line.split(':')[0]
            if name == "Scene" or name == "Credits sequence.\n" :
                continue
            text = only_letters(line.split(':')[1]).lower().strip()

            sub, count = parse_by_words(name, text, subtitle_list, subtitle_index)   
            subtitle_index += count
            new_script.write(str(sub))




if __name__ == "__main__":
    main()