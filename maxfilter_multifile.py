import os
import time
from subprocess import check_output, STDOUT, Popen, PIPE
import easygui
from datetime import datetime

def check_exit(choice):
    if choice is None:
        print('Clicked exit button => exiting.', flush=True)
        raise SystemExit()

def list_fif_files_subfolders(folder):
    fif_files = []
    for path, subdirs, files in os.walk(folder):
        #if 'tmp' in path and 'desktop' in path.lower(): break
        fif_files += [os.path.join(path, filename) for filename in files if filename.endswith('.fif') and not ('sss' in filename)]
    return fif_files

def check_split_file(files):
    """detects and separates file parts, i.e. -1.fif, -2.fif etc """
    files_parts = []
    for file in files:
        for i in range(1, 9999): 
            possible_file_part = f'-{i}'.join(os.path.splitext(file))
            if os.path.exists(possible_file_part):
                files_parts.append(possible_file_part)
            else:
                break
    files = [file for file in files if not file in files_parts]
    return files, files_parts              
                
default_dir = '/neuro/data/sinuhe/'

check_exit(easygui.msgbox('This script for filtering multiple FIF files at once envokes sequential calls to the maxfilter program by MEGIN. Even though all parameters have been tested and produce bitwise equivalent files to the original maxfilter GUI, there is no liability provided with this script. Use this program at your own risk. \n\nChangelog:\n[2022.11] You can now also select entire folders or many files from different locations.\n[2023.10] Filtering of split files now works, as well as disabling autobad\n\nThe script was created by Simon Kern (simon.kern@zi-mannheim.de) in 2021.'))

files = []  # base fif files
files_split = []  # split files are ending in -1, -2, ..., list them here
files_str = ''
while (choice:=easygui.indexbox(f'There are {len(files)} file(s) on the queue:\n\n--------\n{files_str}\n--------\n\nDo you want to add more files or folders?', choices=['Add f[i]les', 'Add f[o]lders', 'Continue']))!=2:
    check_exit(choice)
    seldir = '--directory ' if choice==1 else ''
    str_seltype = 'folders' if choice==1 else 'files'
    zenity_filechooser = f'zenity --file-selection --multiple --filename={default_dir} {seldir}--title "Select {str_seltype} for MaxFiltering" --file-filter=*.fif'
    try:
        files_sel = check_output(zenity_filechooser, shell=True)
    except:
        continue
    files_sel = files_sel.strip().decode().split('|')
    for file_sel in files_sel:
        if os.path.isdir(file_sel):
            files_added = list_fif_files_subfolders(file_sel)
        elif os.path.isfile(file_sel):
            files_added = files_sel
        else:
            raise Exception(f'File is neither file nor dir: {file_sel}')
        for file in files_added: # make sure not to include duplicates
            if file not in files:
                files.append(file)
                
    # automatically detect file parts and separate them.
    files, files_parts = check_split_file(files)
    
    files_str = '\n'.join(['/'.join(f.split('/')[-3:]) for f in files])
    if files_parts:
        files_str += f'\n\n({len(files_parts)} split file(s) detected (i.e., "-1.fif" etc.). Only displaying base files).\n'
    if len(files)>100:
        files_str = '(scroll down to see all files)\n' + files_str

if len(files)==0:
    raise Exception("Please select at least one file.")

p_mode = easygui.buttonbox("Run SSS or tSSS?", choices=["SSS", "tSSS"])
check_exit(p_mode)
p_move = easygui.buttonbox("Run movement correction?", choices=["yes", "no"])
check_exit(p_move)
p_autobad = easygui.buttonbox("Scan for bad channels?\n\n(not recommended if large artifacts are present, e.g. braces or metal parts that would need tSSS for fixing.). Default is on for SSS and off for tSSS.", choices=["on", "off", "default"])
check_exit(p_autobad)
p_head = easygui.buttonbox("Use initial head position or transform to default?\n(Megin guy said: \"don't use default position, it's unstable\")", choices=["initial", "default", "from other file"])
check_exit(p_head)

maxfilter_template = "nice /neuro/bin/util/maxfilter -gui -f {0} -o {1}"

## default settings
if p_mode=='': p_mode = 'tSSS'
if p_move=='': p_move = 'yes'
if p_head=='': p_head = 'initial'
if p_autobad=='': p_autobad = 'on'

p = ''
file_ending = ''
    
if p_head=='default':
    p += ' -trans default'
    file_ending += '_default'
elif p_head=='initial':
    file_ending += '_initial'
elif p_head=='from file':
    zenity_filechooser = 'zenity --file-selection --filename={0} --title "Select FIF file for head position tranformation reading" --file-filter=*.fif'.format(files[0])
    headpos_file = check_output(zenity_filechooser, shell=True)
    headpos_file = headpos_file.strip().decode()
    p += ' -trans {}'.format(headpos_file)
    file_ending += '_trans[{}]'.format(os.path.splitext(os.path.basename(headpos_file))[0])

if p_mode=='tSSS':
    p += ' -st'
    file_ending += '_tsss'
else:
    file_ending += '_sss' 

if p_move=='yes': 
    p += ' -movecomp'
    file_ending += '_mc'

if p_autobad=='off':  # on by default
    p += ' -autobad off'
elif p_autobad=='on':
    p += ' -autobad on'

print('params: ', p)
maxfilter_template = maxfilter_template + p

proj_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(files[0]))))
msg_copy = f"Copy filtered files automatically to Hobbes?\nWill be copied to //hobbes/daten/MaxFiltered/{proj_name}/*.\nMake sure to copy the files from hobbes to your own server storage. To save space on the MEG machine it's advised to delete the tSSS files once they're copied to hobbes. \n\n Source files will NEVER be deleted from sinuhe, ONLY the filtered files."
if any([' ' in file for file in files]):
    msg_copy += '\n\nWARNING: Some files contain spaces, cannot copy these files to hobbes'
p_copy = easygui.buttonbox(msg_copy, choices=["copy to hobbes and delete (t)SSS files on sinuhe\n(keep originals)", "copy to hobbes but keep everything", "no"])
check_exit(p_copy)

commands = []
warn_exist = []
file_outs = []
for i, file in enumerate(files):
    filebase = os.path.splitext(file)[0]
    file_out = filebase + file_ending + '.fif'
    if os.path.exists(file_out): warn_exist += [file_out]
    file_outs.append(file_out)
    maxfilter_cmd = maxfilter_template.format(file, file_out)
    commands.append(maxfilter_cmd)
    
# dont forget to also enumerate the split files for later copy
for i, file in enumerate(files_parts):
    filebase, i_part = os.path.splitext(file)[0].rsplit('-', 1)
    file_out = filebase + file_ending + f'-{i_part}.fif'
    if os.path.exists(file_out): warn_exist += [file_out]
    file_outs.append(file_out)

msg_filter = maxfilter_template.format("[INPUT_FILE]", "[OUTPUT_FILE]")
zenity_info = f'zenity --info --no-wrap --text "running the following command on {len(files)} files:\n\n{msg_filter}" '
check_output(zenity_info, shell=True).decode().split('|')

if warn_exist != []:
    zenity_question = 'zenity --question --no-wrap --text "Warning, some of the files already exist.\n\nFiles:\n{0}\n\nNo overwrite is possible with maxfilter! Script will exit now." '.format('\n'.join(warn_exist))
    check_output(zenity_question, shell=True).decode().split('|')
    raise Exception

# create a list of commands that we are going to run, for each file one new line
msg_start = 'echo "####### Running with the following parameters: {0} \n'.format(p)
msg_start += 'echo "#######  {0} \n'.format(("No copy to hobbes." if p_copy=='no' else "Will copy to Hobbes. ") + ("Delete filtered files on sinuhe. Original raw files will not be deleted." if "delete" in p_copy else ""))
cmd = '\n'.join([msg_start] + ['echo "# running {0}/{1} ({2}), {3}" ; cd \'{4}\' ; {3} 1>&2'.format(i+1, len(files), os.path.basename(fc[0]), fc[1], os.path.dirname(fc[0])) for i, fc in enumerate(zip(files, commands))])
cmd += '\necho "# MaxFiltering of {0} file(s) done! See terminal for potential error messages."'.format(len(files))

run_command = f'(\n{cmd}\n) | \n zenity --progress {"--auto-close" if p_copy else ""} --auto-kill --width 500 --title "Running MaxFilter" --text=="Running MaxFilter"'

p = Popen(run_command, shell=True, stderr=PIPE)

# write all console output to a logfile in the same output folder
proj_name = os.path.dirname(os.path.dirname(os.path.dirname(file_outs[0])))
curr_date = datetime.now().strftime('%Y%m%d-%H-%M')
logfile = os.path.join(proj_name, f'maxfilter_{curr_date}.log')
with open(logfile, 'w') as f:
    f.writelines('[{}] Starting MaxFilterMultifile for the following files: {}'.format(time.ctime(), files))
    f.writelines('\nn\Running command: {} \n\n'.format(run_command))
    while p.poll() is None:
        line = p.stderr.readline().decode()
        print(line, end='')
        f.writelines(line)
    f.write('\n\nFinished at {}!'.format(time.ctime()))
print("Finished!")


if p_copy!="no": # this means copy files to here
    raise Exception('Only applicable for within ZI use')
