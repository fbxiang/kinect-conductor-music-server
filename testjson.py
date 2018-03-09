from midi import Midi
import json
import numpy as np
import os

def convertInstrument(ins):
    print(ins)
    if ins == 0:
        return -1
    if ins == 1: # left
        return 1
    if ins == 2: # right
        return 0
    return 0

def process(name):
    md = Midi()
    notes = {}

    with open(name + '.json', 'r') as f:

        json_data = json.load(f)

        for cell in json_data['cells']:
            if cell['type'] == 'basic.Rect':
                notes[cell['id']] = {"chord": cell['chord'], "next": None, "prev": None}

        for cell in json_data['cells']:
            if cell['type'] != 'basic.Rect':
                notes[cell['source']['id']]['next'] = cell['target']['id']
                notes[cell['target']['id']]['prev'] = cell['source']['id']

    sources  = [i for i, n in notes.items() if n['prev'] is None]
    sinks = [i for i, n in notes.items() if n['next'] is None]

    paths = []
    for curr_id in sources:
        length = 0
        path = { "Length": 0, "Notes": [], "Instrument": -1}
        while curr_id is not None:
            chord = notes[curr_id]['chord']
            for note in chord['notes']:
                assert note['startTime'] >= 0 and note['startTime'] < chord['duration']
                path['Notes'].append({"Note": md.convert_note(note['key']), "Time": note['startTime'] + length})
            if path['Instrument'] == -1 and len(chord['instruments']) > 0 and chord['instruments'][0] != 0:
                path['Instrument'] = convertInstrument(chord['instruments'][0])
            curr_id = notes[curr_id]['next']
            length += chord['duration']
        path['Length'] = length
        paths.append(path)

    # assert the length is unique for each path
    assert len(set([p['Length'] for p in paths])) == 1

    for p in paths:
        for n in p['Notes']:
            n['Instrument'] = p['Instrument'] if p['Instrument'] >= 0 else 1

    all_notes = []
    for p in paths:
        all_notes += p['Notes']
    all_notes = sorted(all_notes, key=lambda n: n['Time'])

    notemap = {}
    for note in all_notes:
        if (note['Instrument'], note['Time']) not in notemap:
            notemap[(note['Instrument'], note['Time'])] = []
        notemap[(note['Instrument'], note['Time'])].append(note)
    all_notes2 = []
    for ins_time, notes in notemap.items():
        all_notes2.append({"Instrument": ins_time[0], "Time": ins_time[1], 'Notes': [n['Note'] for n in notes]})
    all_notes2 = sorted(all_notes2, key=lambda n: n['Time'])

    combined = {"Length": paths[0]['Length'], "Notes": all_notes}
    combined2 = {"Length": paths[0]['Length'], "Notes": all_notes2}

    assert combined2['Length'] % 64 == 0
    # print(combined2)

    try:
        os.mkdir('v1')
        os.mkdir('v2')
    except:
        pass

    with open('v1/' + name + '.json', 'w') as f:
        json.dump(combined, f)

    with open('v2/' + name + '.json', 'w') as f:
        json.dump(combined2, f)


def processAll():
    for name in [f[:-5] for f in os.listdir() if ".json" in f]:
        process(name)


if __name__ == '__main__':
    processAll()
