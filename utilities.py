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
                    self.files.append(os.path.join(root, file))

    def convert(self):
        c = 0
        for file in self.files:
            with codecs.open(file, "r", "utf_8_sig") as f:
                filedata = f.read()
                string_pattern = r'([\/-]\S*\.[jpg|png|gif]{3})'
                static_pattern = r'{%\s*static'
                result = re.findall(string_pattern, filedata)
                result_static = re.findall(static_pattern, filedata)
                # replace = f"{{% static '{file_name}' %}}"
                if result and not result_static:
                    c+=1
                    print('*******************************')
                    print('FILE {}'.format(c), file)
                    print('FOUND', result)
                    for res in result:
                        replacer = f"{{% static '{res[1:]}' %}}"
                        print('found', res, 'replacing', replacer)
                        new_file_data = re.sub(res, replacer, filedata)
                        filedata = new_file_data
                    # print('filename', file)
                    # print('splitting', file.split('.'))
                    # print('new_filename', "_new.html".join(file.split('.html')))
                    with open("_new.html".join(file.split('.html')), 'w', newline='', encoding='utf8') as new_file:
                        new_file.write(new_file_data)

                # # Replace the target string
                # filedata = filedata.replace('ram', 'abcd')

                # # Write the file out again
                # with open('file.txt', 'w') as file:
                # file.write(filedata)
                # lines = f.readlines()
                # for line in lines:
                    # print(line)
                    # if not exclude_static.search(line):
                        # if string_pattern.search(line):
                        # print(line)
                        # file_name_pattern = re.compile('[\"\']([\/-])(\S).*\.(jpg|png|gif)[\"\']')
                        # file_name_pattern = re.compile('([\/-])(\S)*\.(jpg|png|gif)')
                            # try:
                                # print(exclude_static.search(line).group())
                                # print(string_pattern.search(line).group())
                                # old_file_name = string_pattern.search(line).group()
                                # if old_file_name.startswith('/'):
                                    # new_file_name = old_file_name[1:]
                                    # print(new_file_name)
                                    # line.replace(old_file_name, f"{{% static '{new_file_name}'}}")
                                    # print(old_file_name, f"{{% static '{new_file_name}' %}}")
                                    # line.replace(old_file_name, f"{{% static '{new_file_name}' %}}")
                                # else:
                                    # print(old_file_name, f"{{% static '{old_file_name}' %}}")
                                    # line.replace(old_file_name, f"{{% static '{old_file_name}' %}}")

                                # print(line)
                                # image_file = file_name_pattern.search(line).group()
                                # print('file:', image_file)
                                # print('line:', line)
                            # except Exception as e:
                                # print('EXCEPTION', e)



if __name__ == "__main__":
    analyze = StrAnalyze()
    analyze.find_files()
    analyze.convert()
