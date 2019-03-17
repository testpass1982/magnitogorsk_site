import glob, os, re
import codecs

class StrAnalyze:
    def __init__(self):
        self.string = ''
        self.parameters = ''
        self.files = []

    def find_files(self):
        for root, dirs, files in os.walk(".\mainapp"):
            for file in files:
                if file.endswith(".html"):
                    # print('found a file', os.path.join(root, file))
                    self.files.append(os.path.join(root, file))
                    # print('added to self files')

    def convert(self):
        string_pattern = re.compile('([\/-])(\S)*\.(jpg|png|gif)')
        exclude_static = re.compile('static')
        for file in self.files:
            with codecs.open(file, "r", "utf_8_sig") as f:
                # Read in the file
                # with open('file.txt', 'r') as file :
                # filedata = file.readlines()

                # # Replace the target string
                # filedata = filedata.replace('ram', 'abcd')

                # # Write the file out again
                # with open('file.txt', 'w') as file:
                # file.write(filedata)
                lines = f.readlines()
                for line in lines:
                    # print(line)
                    if not exclude_static.search(line):
                        if string_pattern.search(line):
                        # print(line)
                        # file_name_pattern = re.compile('[\"\']([\/-])(\S).*\.(jpg|png|gif)[\"\']')
                        # file_name_pattern = re.compile('([\/-])(\S)*\.(jpg|png|gif)')
                            try:
                                # print(exclude_static.search(line).group())
                                # print(string_pattern.search(line).group())
                                old_file_name = string_pattern.search(line).group()
                                if old_file_name.startswith('/'):
                                    new_file_name = old_file_name[1:]
                                    print(new_file_name)
                                    # line.replace(old_file_name, f"{{% static '{new_file_name}'}}")
                                    print(old_file_name, f"{{% static '{new_file_name}' %}}")
                                    line.replace(old_file_name, f"{{% static '{new_file_name}' %}}")
                                else:
                                    print(old_file_name, f"{{% static '{old_file_name}' %}}")
                                    line.replace(old_file_name, f"{{% static '{old_file_name}' %}}")

                                # print(line)
                                # image_file = file_name_pattern.search(line).group()
                                # print('file:', image_file)
                                # print('line:', line)
                            except Exception as e:
                                print('EXCEPTION', e)
                            
                # f.close()
                # with open(file 'w') as file:
                # file.write(filedata)


if __name__ == "__main__":
    analyze = StrAnalyze()
    analyze.find_files()
    analyze.convert()
