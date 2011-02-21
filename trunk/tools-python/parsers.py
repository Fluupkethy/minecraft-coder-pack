import csv

def parse_config(filename, renamer_options, miss_crit=True, unk_crit=True):
    ff = open(filename, 'r')

    while True:
        buffer = ff.readline()
        
        if not buffer:
            break
            
        buffer = buffer.split('=')

        if buffer[0].strip() in renamer_options:
            renamer_options[buffer[0].strip()] = buffer[1].strip()
        elif buffer[0].strip() == '':
            continue
        else:
            if unk_crit:
                raise KeyError('Unknown keyword in config file : %s'%buffer[0].strip())
            else :
                print ('Unknown keyword in config file : %s'%buffer[0].strip())
            
    for i in renamer_options.keys():
        if not renamer_options[i]:
            if miss_crit:
                raise KeyError('Missing option in config file : %s'%i)
            else:
                print ('Missing option in config file : %s'%i)
            
    return renamer_options

def parse_csv   (filename, header_size, symbol, fields):
    print '+ Opening file %s for reading.'%filename
    csv_file = csv.reader(open(filename, 'rb'), delimiter=symbol)
    
    for i in range(header_size):
        csv_file.next()
    
    #We skip the header
    csv_list = []

    while True:
        try:
            line = csv_file.next()
        except:
            break

        while len(line) < len(fields):
            line.append('*')

#        if len(line) >= len(fields):
        line_dic   = {}
            
        for j in range(len(line)):
            if not line[j]:
                line[j] = '*'
            
        for j in range(len(fields)):
            line_dic[fields[j]] = line[j].strip()

        csv_list.append(line_dic)

    return csv_list

def parse_rgs   (filename):
    
    print '+ Opening file %s for reading.'%filename
    ff = open(filename, 'rb')

    rgs_keywords = {'.option':    ['rgs_name'], 
                    '.class_map': ['src_name', 'trg_name'], 
                    '.method_map':['src_name', 'src_sig', 'trg_name'], 
                    '.field_map': ['src_name', 'trg_name'],                    
                    '.class':     ['src_name', 'arg'],
                    '.field':     ['src_name', 'src_type', 'arg'],
                    '.method':    ['src_name', 'src_sig',  'arg'],
                    '.attribute': ['src_name', 'arg']
                    }

    parsed_dic   = {'option':[],
                    'class_map':[],
                    'method_map':[],
                    'field_map':[],
                    'class':[],
                    'field':[],
                    'method':[],
                    'attribute':[]
                    }

    def get_parsed_line(keyword, buffer):
        return dict(zip(rgs_keywords[keyword], [i.strip() for i in buffer]))


    while True:
        
        buffer = ff.readline()
        if not buffer:
            break
 
        buffer = buffer.split(' ')
        #If we have a comment, we skip
        if buffer[0][0] == '#' or buffer[0].strip() == '':
            continue
            
        #If we have a known keyword
        if buffer[0] in rgs_keywords:
            parsed_dic[buffer[0][1:]].append(get_parsed_line(buffer[0], buffer[1:]))
        else:
            raise KeyError('Error parsing RGS file %s. Keyword %s not recognized.'%(filename, buffer[0]))
 
    ff.close()
    
    return parsed_dic

def parse_saffx (filename):

    print '+ Opening file %s for reading.'%filename
    ff = open(filename, 'rb')

    saffx_states = {  '[OPTIONS]': ['command', 'argument'],
                      '[CLASSES]': ['src_name', 'trg_name'], 
                      '[METHODS]': ['src_name', 'src_sig', 'trg_name', 'trg_sig'], 
                      '[FIELDS]':  ['src_name', 'trg_name']
                    }

    parsed_dic   = {
                      'options':[],
                      'classes':[],
                      'methods':[],
                      'fields':[],
                    }

    def get_parsed_line(keyword, buffer):
        return dict(zip(saffx_states[keyword], [i.strip() for i in buffer]))


    current_state = None
    current_key   = None
    while True:
        buffer = ff.readline()
        if not buffer:
            break
        
        if buffer.strip() in saffx_states:
            current_state = buffer.strip()
            current_key   = current_state.replace('[', '').replace(']', '').lower()
            continue

        if buffer[0] == '#' or buffer.strip() == '':
            continue

        buffer = buffer.split(' ')
        #buffer = re.split(' |.', buffer)
            
        parsed_dic[current_key].append(get_parsed_line(current_state, buffer))
 
    ff.close()

    return parsed_dic
