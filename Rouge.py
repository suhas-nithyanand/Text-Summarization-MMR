#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyrouge import Rouge155
import json

if __name__ == "__main__":

    # You need to modify the following directories
    # to make pyrouge run properly on your machine
    rouge_dir = '/home/suhas/ucf/2ndsem/nlp/4th_assign/HW4/RELEASE-1.5.5/'
    rouge_args = '-e /home/suhas/ucf/2ndsem/nlp/4th_assign/HW4/RELEASE-1.5.5/data -n 4 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -a -x -l 100'

    rouge = Rouge155(rouge_dir, rouge_args)

    # 'model' refers to the human summaries
    rouge.model_dir = '/home/suhas/ucf/2ndsem/nlp/project/Final_Project/Human_Summaries/eval/'
    rouge.model_filename_pattern = 'D3#ID#.M.100.T.[A-Z]'

    # 'system' or 'peer' refers to the system summaries
    # We use the system summaries from 'ICSISumm' for an example
    rouge.system_dir = '/home/suhas/ucf/2ndsem/nlp/project/mmr_final/summaries/'
    rouge.system_filename_pattern = 'd3(\d+)t.txt'

    rouge_output = rouge.evaluate()
    output_dict = rouge.output_to_dict(rouge_output)

    print json.dumps(output_dict, indent=2, sort_keys=True)
