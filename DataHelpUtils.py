#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:bjlizhipeng
# fastext 输入数据加工处理

import os, argparse
import re
#TOKENIZER_RE = re.compile(r"[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Z]{2,}(?![a-z])|[A-Z][a-z]+(?=[A-Z])|[\'\w\-]+",
#                         re.UNICODE)
# TOKENIZER_RE = re.compile(r"[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Za-z]{2,}|[\'\w\-]+",
#                          re.UNICODE)
split_re_str = u'[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Za-z]{1,}|[\'\-]+|\d+'
TOKENIZER_RE = re.compile(split_re_str)
def tokenizer(iterator):
  """Tokenizer generator.
  Args:
    iterator: Input iterator with strings.

  Yields:
    array of tokens per each value in the input.
  """
  for value in iterator:
    yield TOKENIZER_RE.findall(value)

def read_file(input_file, out_file, split_label=",,", split_text=" ", batch_size=10000):
    total_line = 0
    error_line = 0
    with open(input_file, 'r') as f_input, open(out_file, 'w') as f_out:
        for line in f_input.readlines():
            total_line += 1
            arr = line.split(",,")
            if len(arr) != 2 :
                print("第{}行格式错误:{}".format(total_line,line))
                error_line += 1
                continue
            text = TOKENIZER_RE.findall(arr[1])
            # label split_label text(os.linesep) example:__label__16,,发现一个bug \n
            out_line = "{}{}{}{}".format(arr[0], split_label, str(split_text).join(text), os.linesep)
            f_out.write(out_line)
    print("总共处理{}行文本,格式不符合规范的{}行".format(total_line, error_line))

def main():
    parser = argparse.ArgumentParser(description='Fasttext 输入样本预处理')
    parser.add_argument('--input_file', type=str, required=True, help=' 预处理文本的全路径')
    parser.add_argument('--output_file', type=str, default='', help='处理后文件输出目录')
    #parser.add_argument('--out_dir', type=str, default='data_path', help='处理后文件输出目录')
    parser.add_argument('--split_label', type=str, default=',,', help='label 与文本之前的分隔符')
    args = parser.parse_args()
    input_file = args.input_file
    out_file = ""
    file_name = os.path.basename(input_file)
    if not os.path.exists(input_file):
        print("指定的预处理文件不存在!!! --input_file={} ,脚本停止执行".format(input_file))
        exit(-1)
    #输出文件为空,保存到输入目录
    if args.output_file == '':
        print("由于你没有指定输出目录,默认采用输入目录作为输出目录")
        out_dir = os.path.dirname(input_file)
        out_file = os.path.join(out_dir, file_name + ".deal")
    else:
        out_file = args.output_file
        out_dir = os.path.dirname(out_file)
        os.makedirs(out_dir, exist_ok=True)
    if os.path.exists(out_file):
        print("移除目标文件{}".format(out_file))
        os.remove(out_file)
    #输出文件
    read_file(input_file, out_file, split_label=args.split_label)
if __name__ == '__main__':
    #参数解析
    #print(TOKENIZER_RE.findall("我的联系方式是:1383301998,我的 QQ 号码是:20111876997,我要买的鞋是 NB!!!"))
    main()

