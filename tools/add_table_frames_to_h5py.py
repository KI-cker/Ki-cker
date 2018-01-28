from kicker.train import Parser, Converter

p = Parser('train/games.h5')

for g in p.file:
    print("Processing {}".format(g))

    if 'table_frames_encoded' not in p.file[g]:
        del p.file[g]['table_frames_encoded']
        c = Converter(p, g)
        p.file[g]['table_frames_encoded'] = c.get_table_frames_encoded()

p.file.flush()