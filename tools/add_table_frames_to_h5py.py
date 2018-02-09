import argparse

from kicker.train import Parser, Converter

def add_table_frames(filename):
    p = Parser(filename)

    for g in p.file:
        print("Processing {}".format(g))

        if 'table_frames_encoded' not in p.file[g]:
            del p.file[g]['table_frames_encoded']
            c = Converter(p, g)
            p.file[g]['table_frames_encoded'] = c.get_table_frames_encoded()

    p.file.flush()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_file')
    args = parser.parse_args()
    if args.input_file:
        add_table_frames(args.input_file)


if __name__ == '__main__':
    main()