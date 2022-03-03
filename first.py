#create all the grammers here

import ply.lex as lex
import ply.yacc as yacc
import re
import sys
import os

all_date = {}

open_string = '<span\sclass=\"mw-headline\"\sid=\"Pandemic_chronology\">Pandemic\schronology</span>'
end_string = '<span\sclass=\"mw-headline\"\sid=\"Summary\">Summary</span>'

tokens = [
         'START',
         'END',
         'HSTART',
         'HEND',
         'ULSTART',
         'ULEND',
         'LISTART',
         'LIEND',
         'DIVSTART',
         'DIVEND',
         'PSTART',
         'PEND',
        #  'SUPSTART',
        #  'SUPEND',
        #  'SPANSTART',
        #  'SPANEND',
         'ONETOK',
         'GENTOKSTART',
         'GENTOKEND',
         'NAME'
]

def t_START(t):
    r'<span\sclass=\"mw-headline\"\sid=\"Pandemic_chronology\">Pandemic\schronology</span>'
    return t

def t_END(t):
    r'<span\sclass=\"mw-headline\"\sid=\"Summary\">Summary</span>'
    return t   


def t_HSTART(t):
    r"<h3[^>]*>"
    return t  

def t_HEND(t):
    r"</h3>"
    return t        

def t_ULSTART(t):
    r"<ul>"
    return t

def t_ULEND(t):
    r"</ul>"
    return t


def t_LISTART(t):
    r"<li>"
    return t

def t_LIEND(t):
    r"</li>"
    return t    

# def t_DIVSTART(t):
#     r"<div[^>]*>"
#     return t

# def t_DIVEND(t):
#     r"</div>"
#     return t

def t_PSTART(t):
    r"<p[^>]*>"
    return t    

def t_PEND(t):
    r"</p>"
    return t

# def t_SUPSTART(t):
#     r"<sup[^>]*>"
#     return t

# def t_SUPEND(t):
#     r"</sup>"
#     return t    

# def t_SPANSTART(t):
#     r"<span[^>]*>"
#     return t

# def t_SPANEND(t):
#     r"</span>"
#     return t

def t_ONETOK(t):
    r"<[^/]*/>"


def t_GENTOKEND(t):
    r"</[^>]*>"
    

def t_GENTOKSTART(t):
    r"<[^>]*>"
      


def t_SKIP(t):
    r"&\#91;.*&\#93;"
    #print("token found")

def t_NAME(t):
    r'[A-Za-z0-9.+-,;:\(\)]+'
    return t   

    

# def t_(t):
#     r""
#     return t    

# def t_(t):
#     r""
#     return t

# def t_(t):
#     r""
#     return t

# def t_(t):
#     r""
#     return t    










t_ignore = " \t"

def t_error(t):
	t.lexer.skip(1)


def p_start(t):
    '''start : START name content name END'''
    print("reduced")
    

def p_content(t):
    '''content : heading name data
                | heading name data name content'''
    if len(t)==4:            
        t[0]=t[1]+"\n\n"+t[3]
    else:
        t[0]=  t[1]+"\n\n"+t[3] +"\n\n"+t[4]  
    all_date[t[1]]=t[3]    
    #print('*****',t[0])

def p_heading(t):
    '''heading : HSTART name HEND'''
    t[0]=t[2]
    # print(t[0])

def p_data(t):
    '''data : paragraphs name lists name
            | paragraphs name lists name paragraphs name'''
    if len(t)==3:       
        t[0]=t[1]+"\n"+t[2]
    else:
        t[0]=t[1]+"\n"+t[3]  
    # print("11111.  111.   11   data is reduced")     
    # print(t[0])

def p_paragraphs(t):
    '''paragraphs : PSTART name PEND
                  | PSTART name PEND paragraphs''' 
    if len(t)==4:
        t[0]=t[2]
    elif len(t)==5:
        t[0]=t[2]+'\n'+t[4]

    # print("paragraphs")    
    # print(t[0])    

def p_lists(t):
    '''lists : ULSTART lis ULEND
             '''
    if len(t)==4:
        t[0]=t[2]
    # print("****************************printing in lists")
    # print(t[2])    


def p_lis(t):
    '''lis : LISTART name LIEND
           | LISTART name LIEND lis
           | LISTART name ULSTART lis ULEND LIEND
           | LISTART name ULSTART lis ULEND LIEND lis
           ''' 
    if len(t)==4:
        
        t[0]='\t>'+t[2]
    elif len(t)==5:
        t[0]="\t>"+t[2]+"\n"+t[4]  
    elif len(t)==7:
        t[0]="\t"+t[2]+"\n"+t[4]
    else:
        t[0]="\t*"+t[2]+"\n"+t[4]+"\n"+t[7]        
    #print(t[0])     
                            
         

   

def p_name(t):
    '''name : NAME
            | NAME name
            | '''       
    if len(t)==3:
        t[0] = ' '.join(t[1:])
    elif len(t)==2:    
        t[0] = ''.join(t[1])
    else:
        t[0]="" 
    if t[0]=="edit":
        t[0]=""        
                   


# def p_alldiv(t):
#     '''alldiv : div
#               | div alldiv'''
#     # if len(t)==2:
#     #     t[0]=t[1]
#     # elif len(t)==3:
#     #     t[0]=t[1]+t[2]
#     #print(t[0])  
#     # 
#     #   
     
                                    

def p_error(t):
    pass



if __name__ == "__main__":
    f=open("feb2020.html","r")
    text = f.read()
   # print(text[:1000])
    # result = re.search('<span class="mw-headline" id="Pandemic_chronology">[. /n]*Situation Report 13',text)
    # print(result)
    lexer = lex.lex()
    lexer.input(str(text))


    #printing all tokens
    # x = True
    # count = 100
    # for tok in lexer:
    #     if tok.type == "START":
    #         x = False
    #     if x== False and count:
    #         print(tok)
    #         #count-=1

    #     if tok.type == "END":
    #         x = True


    parser = yacc.yacc(start = "start")
    parser.parse(text)

    for key, value in all_date.items():
        print(key,'\n',value)

