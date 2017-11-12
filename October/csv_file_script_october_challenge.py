import csv
import os
from optparse import OptionParser
import sys

def main():
    # Setting up options and parsing arguments
    args = sys.argv[1:]
    parser = OptionParser()
    #all action output will be printed to screen unless -o and a new csv file name to save the output in
    #input options
    # -f takes a path to a csv file on a local system
    parser.add_option('-f', '--file',  type=str, dest='filename',nargs=1)
    # -http-get-file takes a download url to a csv file
    parser.add_option('--http-get-file', type=str, dest='url')
    #-m takes the paths to 2 csv files
    parser.add_option('-m', '--merge-files', type=str, dest='files',nargs=2)
    #action options
    #-g takes a line number
    parser.add_option('-g', '--get-line', dest='ln')
    #-r takes a line number
    parser.add_option('-r', '--remove-line', dest='rln')
    #--filter takes a string of search characters
    parser.add_option('--filter', dest='csvfilter')
    #-c takes a string of search characters and a target column to search in
    parser.add_option('-c', '--columnfilter', dest='csvcolumn',nargs=2)
    #output boolean
    #-o takes a new csv file name to save output of operations to
    parser.add_option('-o', '--output-file', type=str,dest='output', nargs=1)
    (options, args) = parser.parse_args(args)
    inp, act, out = parse(options, args)
    #operations
    #input options
    if options.filename:
        csv_file = get_file(options.filename)
    if options.files:
        csv_file = merge_files(options.files)
    if options.url:
        csv_file = get_file_online(url)
    #action options
    if options.ln:
        print_text(csv_file, options.ln, out)
        sys.exit()
    if options.rln:
        remove_line(csv_file, options.rln, out)
        sys.exit()
    if options.csvfilter:
        csv_filter(csv_file, options.csvfilter, out)
        sys.exit()
    if options.csvcolumn:
        csv_filter_column(csv_file, options.csvcolumn[0], out, options.csvcolumn[1])
        sys.exit()
# ensures proper input
def parse(options, args):
    inp_count = 0
    act_count = 0
    inp_list = [['filename', options.filename], ['url', options.url], ['files', options.files]]
    act_list = [['ln', options.ln], ['rln', options.rln], ['csvfilter', options.csvfilter], ['csvfilter_column', options.csvcolumn]]
    out = False
    if options.output:
        out = [True, options.output]
    for i in range(0,3):
        if inp_list[i][1]:
            inp_count += 1
            inp = inp_list[i]
        if act_list[i][1]:
            act_count += 1
            act = act_list[i]
    if act_count != 1:
        print 'Must choose a single option from action list: --line_num, --r_line_num, or --filter. --help for help'
        if inp_count != 1:
            print 'Must choose a single option from input list: --file, --http-get-file, or --merge-files. --help for help'
        sys.exit()
    if inp_count != 1:
        print 'Must choose a single option from input list: --file, --http-get-file, or --merge-files. --help for help'
        sys.exit()
    return inp, act, out

def get_file(file_path):
    #readies a local csv file for an action operation
    csvfile = open(file_path, 'rb')
    csv_unchained = csv.reader(csvfile)
    return csv_unchained

def get_file_online(url):
    #downloads and readies a csv file for an action operation
    dl_name = url[url.find('/'):]
    urllib.urlretrieve(url, dl_name)
    return get_file(dl_name)

# all output is printed unless -o is supplied

def merge_files(files):
    # merges two csv files and passes to an action operation
    #first open the files
    file1 = files[0]
    file2 = files[1]
    csvf1 = get_file(file1)
    csvf2 = get_file(file2)
    # creating a filename for the merged file, pre action
    name1 = file1.find('\\', -1)
    name11 = file1.find('.', -1)
    name1 = file1[name1:name11]
    name2 = file2.find('\\', -1)
    name22 = file2.find('.', -1)
    merged_filename = str(name1) + '_' + str(name2) + '.csv'
    merged_file = open(merged_filename, 'w')
    csv_merged_file = csv.writer(merged_file)
    for line in csvf1:
        csv_merged_file.writerow(line)
    for line in csvf2:
        csv_merged_file.writerow(line)
    print 'temporary merged file saved as:', merged_filename
    return csv_merged_file

def remove_line(csv_file, ln, out):
    #takes a specific line and prints it or stores all other lines in a new csv file
    if isinstance(out, list) == True:
        i = 0
        new_file = open(out[1], 'wb')
        new_file_csv = csv.writer(new_file)
        for line in csv_file:
            if i != int(ln):
                new_file_csv.writerow(line)
            i += 1
        print 'Removed line %s in file %s' % (ln, out[1])
    else:
        print_text(csv_file, ln, out)
    return

def print_text(csv_file, ln, out):
    #outputs an indicated line number
    i = 0
    for line in csv_file:
        if i == int(ln):
            if isinstance(out, list)==True:
                try:
                    new_file = open(out[1],'w')
                    new_file_csv = csv.writer(new_file)
                    new_file_csv.writerow(line)
                    print 'Saved line %s in %s' % (ln, out[1])
                    return
                except IOError:
                    error('IOError')
            else:    
                print 'Here is the line:' + str(line)
                return
        i += 1
    error('ln')
    return 
    


def csv_filter(csv_file, key, out):
    #outputs all lines matching a certain key
    if isinstance(out, list) == True:
        new_file = open(out[1],'w')
        new_file_csv = csv.writer(new_file)
        for line in csv_file:
            for item in line:
                if key in item:
                    new_file_csv.writerow(line)
        print 'Saved search results of %s in %s' % (key, out[1])
        return
    else:
        for line in csv_file:
            for item in line:
                if key in item:
                    print line

    return
def csv_filter_column(csv_file, key, out, column_num):
    #outputs all lines that have an indicated column matching the key
    if isinstance(out, list) == True:
        new_file = open(out[1],'w')
        new_file_csv = csv.writer(new_file)
        for line in csv_file:
            if key in line[int(column_num)]:
                new_file_csv.writerow(line)
        print 'Saved search results of %s in %s' % (key, out[1])
        return
    else:
        for line in csv_file:
            if key in line[int(column_num)]:
                    print line
    
def error(error_type):
    error_dict = {'ln':'Error: Line number cannot be negative or higher than the last line of text', 'IOError': 'Error: Invalid file path',}
    print error_dict[error_type]
    sys.exit()

main()
    


