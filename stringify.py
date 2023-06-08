import numpy as np


def stringify(story, exist_answer=False):

    lines = []

    i = 0  # The number of descriptions processed
    j = 0  # The number of lines output

    while True:

        
        if isinstance(story[i], str):
            line = story[i]
        else:
            line = story[i].render()
            # Capitalize the line
            line = line[0].upper() + line[1:]

            # Prepend the line number
            if not line.split()[0] == 'Question:':
                line = '%d %s' % (i + 1, line)
            
            # Append supporting lines indices if necessary
            # if hasattr(story[i], 'idx_support') and story[i].idx_support:
            #     line += '\t%s' % ' '.join([str(x + 1)
            #                             for x in story[i].idx_support])
        
        if exist_answer or not line.split()[0] == 'Answer:':
            lines.append(line)
        
        # Increment counters
        i += 1
        j += 1

        if i >= len(story):
            break

    return lines
