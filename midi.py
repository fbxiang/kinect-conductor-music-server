class Midi:


    def __init__(self):

        s = 'C	C#	D	D#	E	F	F#	G	G#	A	A#	B'

        s_ = s.split()

        note_map = {}
        for i,e in enumerate(s_):

            note_map[e] = i

        self.note_map = note_map


    def convert_note(self, note):

        import re

        notes = re.match("(\D+)(\d)", note).groups()

        num = self.note_map[notes[0]] + ((int)(notes[1]) +1)*12

        return num










