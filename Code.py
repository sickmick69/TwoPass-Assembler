main_opcode = {"CLA": "0000", "LAC": "0001", "SAC": "0010", "ADD": "0011", "SUB": "0100", "BRZ": "0101", "BRN": "0110",
               "BRP": "0111", "INP": "1000", "DSP": "1001", "MUL": "1010", "DIV": "1011", "STP": "1100"}
location_counter = 1                                             # TO GENERATE SPECIFIC ADDRESS
used_opcode = []                                                 # STORES EVERY OPCODE PRESENT IN INSTRUCTIONS
variables = {}                                                   # VARIABLES WITH RESPECTIVE ADDRESS
vari = []                                                        # TO STORE VARIABLES
instructions = []                                                # TO STORE EVERY INSTRUCTION BY LINE
dec_labels = {}                                                  # TO STORE DECLARED LABELS
labels = []                                                      # TO STORE LABEL NAMES
var_address = []                                                 # ADDRESS OF EVERY SINGLE INSTRUCTION FOR MACH. CODE
error_list = []                                                  # TO STORE ALL ERRORS (IF PRESENT)
line = 0                                                         # TO KEEP A TRACK ON EVERY LINE


def bin_convert(num):
    return format(int(num), '08b')


def initialize():
    print("Enter File Name : ")
    filename = input()
    with open(filename) as f:
        global instructions
        instructions = [line.strip() for line in f]

initialize()
if len(instructions) > 1:
    for i in range(len(instructions)):
        if ":" in instructions[i]:
            index = instructions[i].find(":")
            s = instructions[i]
            s = s[0:index]
            if s not in dec_labels.keys():
                dec_labels[s] = bin_convert(location_counter)
            else:
                error_list.append("Label defined multiple times")
            if location_counter > 256:
                error_list.append("Overflow Error")
            location_counter = location_counter + 1


for i in instructions:
    if "//" in i:
        ind = i.find("//")
        if ind == 0:
            instructions.pop(instructions.index(i))
        else:
            instructions[instructions.index(i)] = i[0:ind]


def use_opcode(string):
    global location_counter
    global line
    if location_counter > 256:
        error_list.append("Overflow Error")
    if "\\" not in string:
        if "ADD" in string:
            if string[4:] not in dec_labels.keys():
                if "ADD" not in used_opcode:
                    used_opcode.append("ADD")
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode["ADD"], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif "SUB" in string:
            if string[4:] not in dec_labels.keys():
                if "SUB" not in used_opcode:
                    used_opcode.append("SUB")
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode["SUB"], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif "LAC" in string:
            if string[4:] not in dec_labels.keys():
                if "LAC" not in used_opcode:
                    used_opcode.append("LAC")
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode["LAC"], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif "SAC" in string:
            if string[4:] not in dec_labels.keys():
                if "SAC" not in used_opcode:
                    used_opcode.append("SAC")
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode["SAC"], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif string[0:3] == "DSP":
            if string[4:] not in dec_labels.keys():
                if "DSP" not in used_opcode:
                    used_opcode.append("DSP")
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode["DSP"], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif "INP" in string:
            if string[4:] not in dec_labels.keys():
                if "INP" not in used_opcode:
                    used_opcode.append("INP")
                if len(string) > 4:
                    if string[4:] in variables.keys():
                        error_list.append("Variable already declared at line " + str(line))
                    else:
                        variables[string[4:]] = bin_convert(location_counter)
                        a = [main_opcode["INP"], bin_convert(location_counter)]
                        var_address.append(a)
                        vari.append(string[4:])
                        location_counter = location_counter + 1
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif "BRZ" in string or "BRP" in string or "BRN" in string:
            if string[0:3] not in used_opcode:
                used_opcode.append(string[0:3])
            if len(string) > 3:
                if string[4:] in dec_labels:
                    a = [main_opcode[string[0:3]], dec_labels[string[4:]]]
                    labels.append(string[4:])
                    var_address.append(a)
                else:
                    error_list.append("Label not declared at line " + str(line))
            else:
                error_list.append("Invalid syntax for address in line " + str(line))
        elif "MUL" in string or "DIV" in string:
            if string[4:] not in dec_labels.keys():
                if string[0:3] not in used_opcode:
                    used_opcode.append(string[0:3])
                if len(string) > 3:
                    if string[4:] in variables.keys():
                        a = [main_opcode[string[0:4]], variables[string[4:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Invalid syntax for address in line " + str(line))
            else:
                error_list.append("Labels declared cannot be used a variables at line " + str(line))
        elif ":" in string:
            num = string.find(":")
            sub1 = string[0:num]
            if sub1 not in vari:
                if "STP" in string:
                    a = [dec_labels[sub1], main_opcode["STP"]]
                    var_address.append(a)
                elif "DSP" in string:

                    if string[-1] in variables.keys():

                        a = [dec_labels[sub1], main_opcode["DSP"], variables[string[8:]]]
                        var_address.append(a)
                    else:
                        error_list.append("Variable not declared at line " + str(line))
                else:
                    error_list.append("Limited number of Operands at line " + str(line))
            else:
                error_list.append("Variables declared cannot be used as labels at line " + str(line))
        elif "CLA" in string:
            if string[0:3] not in used_opcode:
                used_opcode.append(string[0:3])
            a = [main_opcode["CLA"], "00000000"]
            var_address.append(a)
        elif "END" in string:
            None
        else:
            if "START" not in string:
                error_list.append("Limited number of opcodes provided at line " + str(line))


# -----------------FIRST PASS----------------------
if len(instructions) <= 1:
    print("Empty input file")
else:
    if "START" not in instructions[0]:
        error_list.append("Does not have a START statement")

    if "END" not in instructions:
        error_list.append("End of the program not found")


for i in range(len(instructions)-1):
    line = i+1
    use_opcode(instructions[i])

file3 = open("OPCODE TABLE.txt", "w")

file3.write("OPCODE TABLE\n")
for i in used_opcode:
    file3.write(i + "\n")
file3.write("--------------")

file = open("SYMBOL TABLE.txt", "w")


file.write("SYMBOL TABLE\n")
file.write("------------\n")
file.write("LABEL TABLE\n")
for i in range(len(labels)):
    file.write(labels[i] + " - " + dec_labels[labels[i]] + "\n")
file.write("------------\n")
file.write("VARIABLES\n")
for i in range(len(vari)):
    file.write(vari[i] + " - " + variables[vari[i]] + "\n")
file.write("------------\n")


#----------------SECOND PASS-----------------

file1 = open("MACHINE CODE.txt", "w")

if len(error_list) > 0:
    print("ERRORS FOUND : ")
    for i in range(len(error_list)):
        print(error_list[i])
else:
    file1.write("MACHINE CODE\n")
    for i in var_address:
        for j in i:
            file1.write(j + " ")
        file1.write("\n")
    file1.write("--------------")

