#!/usr/bin/python
# -*- coding:utf-8 -*-
# author:bjlizhipeng
# fastext 输入数据加工处理

import os, argparse
import re

version="0.003"
#split_re_str = u'[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Za-z]{1,}|[\'\-]+|\d+'
#split_re_str = u'[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Za-z]{1,}|[\'\-]+|\d+[.]{1}\d+|\d+'
split_re_str = u'[\u3400-\u4DB5\u4E00-\u9FA5\uF900-\uFA2C]|[，．？：；！,.?:;!]+|[A-Za-z]{1,}|[\'\-]+|\d+[.]{1}\d+|\d+'
TOKENIZER_RE = re.compile(split_re_str)

def fwidth2hwidth(content):
    '''
    :param content: 字符串
    :return:    半角字符串
    '''
    result = []
    for uchar in content:
        inside_code = ord(uchar)
        # 空格
        if inside_code == 12288:
            inside_code = 32
        # 全角的“”转为 "
        elif inside_code == 8220 or inside_code == 8221:
            inside_code = 34
        # 全角的‘’转为 '
        elif inside_code == 8216 or inside_code == 8217:
            inside_code = 39
        # 其它全角字符串按照换算关系换算
        elif inside_code >= 65281 and inside_code <= 65374:
            inside_code -= 65248

        result.append(chr(inside_code))
    return u''.join(result)


def tokenizer(iterator):
  """Tokenizer generator.
  Args:
    iterator: Input iterator with strings.

  Yields:
    array of tokens per each value in the input.
  """
  for value in iterator:
    yield TOKENIZER_RE.findall(value)


def read_file(input_file, out_file, split_label=",,",
              split_text=" ", full_to_half=False, all_lower=False,
              batch_size=10000):
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
            text = arr[1]
            #如果设置大小写转化,执行
            if all_lower:
                text = text.lower()
            # 如果设置全半角转化,执行
            if full_to_half:
                text =fwidth2hwidth(text)

            text = TOKENIZER_RE.findall(text)
            # label split_label text(os.linesep) example:__label__16,,发现一个bug \n
            out_line = "{}{}{}{}".format(arr[0], split_label, str(split_text).join(text), os.linesep)
            f_out.write(out_line)
    print("总共处理{}行文本,格式不符合规范的{}行".format(total_line, error_line))

def main():
    parser = argparse.ArgumentParser(description='Fasttext 输入样本预处理脚本,当前版本为:'+version)
    parser.add_argument('--input_file', type=str, required=True, help=' 预处理文本的全路径')
    parser.add_argument('--output_file', type=str, default='', help='处理后文件输出目录')
    #parser.add_argument('--out_dir', type=str, default='data_path', help='处理后文件输出目录')
    parser.add_argument('--split_label', type=str, default=',,', help='label 与文本之前的分隔符')
    parser.add_argument('--full_to_half', type=bool, default=False, help='是否全部转化为半角,默认False不转化')
    parser.add_argument('--all_lower', type=bool, default=False, help='是否全部 小写,默认False不转化')
    parser.add_argument('--version', type=str, default=version, help='预处理脚本对应脚本版本号,此参数不用指定,当前版本为:'+version)
    args = parser.parse_args()
    input_file = args.input_file
    print("Fasttext 输入样本预处理脚本,当前版本为:{} ".format(version))
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
    read_file(input_file, out_file, split_label=args.split_label,
              full_to_half=args.full_to_half, all_lower=args.all_lower )
if __name__ == '__main__':
    #参数解析
    # split_re_str_test = u'[\u4e00-\u9fa5]|[，．？：；！,.?:;!]+|[A-Za-z]{1,}|[\'\-]+|\d+[.]\d+|\d+'
    # TOKENIZER_RE_test = re.compile(split_re_str_test)
    # print(TOKENIZER_RE_test.findall("我愛中華人名共和國,衣服12.291456我的联系方式是:1383301998,我的QQ号码是:20111876997,我要买的鞋是NB!!!（￣︶￣）↗"))
    main()

