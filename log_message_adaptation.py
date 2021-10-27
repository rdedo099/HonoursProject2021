import re

from numpy.core.defchararray import startswith

#from main.org.core.utility.message import Message

'''
    change the log message if it contains a specific bloc of words
    that matched a special regular expression
'''


def adapt_log_message(log_message: str, regex=None):
    # first detect time (12:34:56 or 12:54 )
    # date 21-03-2005 03/04/12
    # ip address
    # memory address
    # file path
    # mac address
    # before adding space around ':'
    
     # add space around '-->' [=:,] <> () [ ] { }
    #log_message = re.sub("([<>=:,;'\(\)\{\}\[\]])\"\"", r' \1 ', log_message)
    

    is_ip_address1 = re.findall('(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)', log_message)
    if is_ip_address1:
        log_message = re.sub('(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)', " IP_ADDRESS ", log_message)

    is_ip_address = re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', log_message)
    if is_ip_address:
        log_message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', " IP_ADDRESS ", log_message)

    # date format : mm-/dd-/yyyy or dd-/mm-/yyyy
    is_date1 = re.findall('(^|\s+)(\d{1,2}(-|/)\d{1,2}(-|/)\d{2,4})(\s+|$)', log_message)
    if is_date1:
        log_message = re.sub('(^|\s+)(\d{1,2}(-|/)\d{1,2}(-|/)\d{2,4})(\s+|$)', " DATE ", log_message)
        
    # date format : yyyy-/dd-/mm or yyyy-/mm-/dd
    is_date2 = re.findall('(^|\s+)*(\d{2,4}(-|\/)\d{1,2}(-|\/)\d{1,2})(\s+|$)*', log_message)
    if is_date2:
        log_message = re.sub('(^|\s+)*(\d{2,4}(-|\/)\d{1,2}(-|\/)\d{1,2})(\s+|$)*', " DATE ", log_message)
        
     # date format : dd-/MM-/yyyy
    is_date3 = re.findall(r'(\d{1,2}(-|\/|\s+)*)*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(\s*|-|\/)*(?:[0-9]{2,4})*(?=\D|$)', log_message)
    if is_date3:
        log_message = re.sub(r'(\d{1,2}(-|\/|\s+)*)*(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sept(?:ember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)(\s*|-|\/)*(?:[0-9]{2,4})*(?=\D|$)', " DATE ", log_message)

    is_time = re.findall('(^|\s+)*(\d){1,2}:(\d){1,2}(|:(\d){2,4})(\s+|$)', log_message)
    if is_time:
        log_message = re.sub('(^|\s+)*(\d){1,2}:(\d){1,2}(|:(\d){2,4})(\s+|$)', " TIME ", log_message)
        
    is_time1 = re.findall('((\d){1,2}:(\d){1,2}($|:(\d){2,4}))', log_message)
    if is_time1:
        log_message = re.sub('((\d){1,2}:(\d){1,2}($|:(\d){2,4}))', " TIME ", log_message)
    
        #(^|\s+)*[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}(\s+|$)*
    is_uuid = re.findall(r'\b[0-9a-z]{8}\b-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-\b[0-9a-z]{12}\b', log_message)
    if is_uuid:
        log_message = re.sub(r'\b[0-9a-z]{8}\b-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-\b[0-9a-z]{12}\b', " UUID ", log_message)
        
    is_duid = re.findall('(([0-9a-z]){24,64})', log_message)
    if is_duid:
        log_message = re.sub('(([0-9a-z]){24,64})', " DUID ", log_message)

    is_memory_address = re.findall('0x([a-zA-Z]|[0-9])+', log_message)
    if is_memory_address:
        log_message = re.sub('0x([a-zA-Z]|[0-9])+', " MEMORY_ADDRESS ", log_message)

    is_hex = re.findall('(^|\s)([0-9A-F]){9,}(\s|$)', log_message)
    if is_hex:
        log_message = re.sub('(^|\s)([0-9A-F]){9,}(\s|$)', " HEX ", log_message)

    is_hex1 = re.findall('(^|\s)([0-9a-f]){8,}(\s|$)', log_message)
    if is_hex1:
        log_message = re.sub('(^|\s)([0-9a-f]){8,}(\s|$)', " HEX ", log_message)

    is_mac_address = re.findall('([0-9A-F]{2}[:-]){5,}([0-9A-F]{2})', log_message)
    if is_mac_address:
        log_message = re.sub('([0-9A-F]{2}[:-]){5,}([0-9A-F]{2})', " MAC_ADDRESS ", log_message)
        
    is_host = re.findall('([0-9]{4}-[0-9A-Z]{7})', log_message)
    if is_host:
        log_message = re.sub('([0-9]{4}-[0-9A-Z]{7})', " HOST ", log_message)
        
    is_url = re.findall(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", log_message)
    if is_url:
        log_message = re.sub(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", " URL ", log_message)

    is_file_path = re.findall('(|\w+)(/[\d+\w+\-_\.\#\$]*[/\.][\d+\w+\-_\.\#\$/*]*)+', log_message)
    if is_file_path:
        log_message = re.sub('(|\w+)(/[\d+\w+\-_\.\#\$]*[/\.][\d+\w+\-_\.\#\$/*]*)+', "FILE_PATH", log_message)
        
    is_number = re.findall(r'\b(\d+)\b', log_message)
    if is_number:
        log_message = re.sub(r'\b(\d+)\b', " NUMBER ", log_message)

    # add space around '-->' [=:,] <> () [ ] { }
    #log_message = re.sub("([<>=:,;?'\(\)\[\]]).", r' \1', log_message)
    
    log_message = log_message.translate(str.maketrans({'(': ' ', ')': ' ', '<':' ', '>':' ', '=':' ', ':':' ', ',':' ', ';':' ', '{':' ', '}':' ','[':' ',']':' ','"':' ', '\'':' ', '-':' ', '?':' ', '/':' ', '\\':' ', '.':' ', '|':' ', '*':' ', '\t':'', '%':' ', '”' : ' '}))
    
    log_message = re.sub("(\s{2,})", ' ', log_message)
    
    '''
    # regex is empty if not given as parameter
    if regex is None:
        regex = []
    for i in range(len(regex)):
        match = re.findall(regex[i], log_message)
        if match:
            log_message = re.sub(regex[i], "VAR", log_message)

    
    # let's identify the prefixes that we don't have to change
    prefix_regex = "^[ ]*\[[A-Z *]+\]"
    match = re.findall(prefix_regex, log_message)
    if len(match) > 0:
        log_message = log_message.replace(match[0], match[0].replace(' ', ''))
    
    
    log_message = log_message.replace("-- >", "-->")
    message = Message(log_message.split())

    for index in range(0, message.get_length()):
        match = False
        match = match or re.findall(".xml", message.words[index]) # xml files
        if match:
            message.words[index] = '#spec#'
    '''
    
    return log_message