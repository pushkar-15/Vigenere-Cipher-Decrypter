# (Sample outputs, explanations and decrypted message is included in comments)





from math import sqrt

# open the given files and store the text in variables:
with open('helper-files\mogambo.txt', 'r') as file:
    C = file.read()
with open('helper-files\interval.txt', 'r') as file:
    intervals_lines = [line.rstrip() for line in file]

# list of interval values
intervals = [intervals_lines[i] for i in range(1,len(intervals_lines),2)]
#---------------------------------------------------------------------------------------------------------------------------------




# Implementing Kasiski examination:


def _get_factors(number):
    """
    Returns a sorted list of all factors of a number.
    """
    factors = set()
    for i in range(1, int(sqrt(number))+1):
        if number % i == 0:
            factors.add(i)
            factors.add(number//i)
    return sorted(factors)


def _candidate_key_lengths(factor_lists, max_key_len):
    """
    Returns a list of all possible key lengths, sorted in decsending order based on probability.
    """
    all_factors = [factor_lists[lst][fac] for lst in range(len(factor_lists)) for fac in range(len(factor_lists[lst]))]
    
    # exclude factors larger than suspected maximum key length
    candidate_lengths = list(filter(lambda x:  x <= max_key_len, all_factors))
    
    # sort by frequency (descending)
    sorted_candidates = sorted(set(candidate_lengths), key=lambda x: all_factors.count(x), reverse=True)
    return sorted_candidates


# list of all factors of every element in intervals
mp = []
for interval in intervals:
    factors = _get_factors(int(interval))
    mp.append(factors)

# print our possibilities: (given that Key length <= 20)
print("Possible Key Lengths: ", _candidate_key_lengths(mp, 20))

# output: 
# Possible Key Lengths:  [1, 2, 3, 6, 4, 12, 9, 18, 8, 16, 7, 14, 5, 10, 15, 13, 19, 11, 20, 17]

# From this output we infer that the most probable key lenght is 6. 
# This is because we can see that all the factors and multiples of 6 in the output.
# Hence we assume that Key Length = 6 and proceed.
#---------------------------------------------------------------------------------------------------------------------------------




# Frequency Analysis:


# group the given ciphertext into 6 groups
groups = []
for k in range(6):
    groups.append([C[i] for i in range(k, len(C), 6)])


def character_frequency(char_list):
    """
    Given a list of characters, returns a dictionary containing frequency of each character.
    """
    frequency_dict = {}
    for char in char_list:
        if char in frequency_dict:
            frequency_dict[char] += 1
        else:
            frequency_dict[char] = 1
    return frequency_dict


# f[i] stores the character_frequency dictionary of ith group.
f = []
for i in range(6):
    f.append(character_frequency(groups[i]));


# We print each f[i] and analyse it.
# By comparing these frequencies to the Letter Frequencies in English language, we derive the possible key.
# Hence, Frequency Analysis was performed on each group[i] seperately.


# Guess the Key based on groupwise frequencies:

shifts = [1,17,20,19,20,18] # Derived from Frequency Analysis.
key = [chr(shifts[i] + ord('A')) for i in range(len(shifts))]

print("key =", key)
# output: 
# key = ['B', 'R', 'U', 'T', 'U', 'S']
#---------------------------------------------------------------------------------------------------------------------------------


# Decryption:

def vigenere_decrypt(ciphertext, key):
    """
    Decrypts a Vigenere ciphertext using the provided key.
    """
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            shift = ord(key[i % key_length].lower()) - ord('a')
            if char.isupper():
                decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
            else:
                decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            decrypted_text += char
    return decrypted_text


# decrypted text (plaintext)
M = vigenere_decrypt(C, key)
print(M)

# output:
# BEPATIENTTILLTHELASTROMANSCOUNTRYMENANDLOVERSHEARMEFORMYCAUSEANDBESILENTTHATYOUMAYHEARBELIEVEMEFORMINEHONOURANDHAVERESPECTTOMINEHONOURTHATYOUMAYBELIEVECENSUREMEINYOURWISDOMANDAWAKEYOURSENSESTHATYOUMAYTHEBETTERJUDGEIFTHEREBEANYINTHISASSEMBLYANYDEARFRIENDOFCAESARSTOHIMISAYTHATBRUTUSLOVETOCAESARWASNOLESSTHANHISIFTHENTHATFRIENDDEMANDWHYBRUTUSROSEAGAINSTCAESARTHISISMYANSWERNOTTHATILOVEDCAESARLESSBUTTHATILOVEDROMEMOREHADYOURATHERCAESARWERELIVINGANDDIEALLSLAVESTHANTHATCAESARWEREDEADTOLIVEALLFREEMENASCAESARLOVEDMEIWEEPFORHIMASHEWASFORTUNATEIREJOICEATITASHEWASVALIANTIHONOURHIMBUTASHEWASAMBITIOUSISLEWHIMTHEREISTEARSFORHISLOVEJOYFORHISFORTUNEHONOURFORHISVALOURANDDEATHFORHISAMBITIONWHOISHERESOBASETHATWOULDBEABONDMANIFANYSPEAKFORHIMHAVEIOFFENDEDWHOISHERESORUDETHATWOULDNOTBEAROMANIFANYSPEAKFORHIMHAVEIOFFENDEDWHOISHERESOVILETHATWILLNOTLOVEHISCOUNTRYIFANYSPEAKFORHIMHAVEIOFFENDEDIPAUSEFORAREPLYTHENNONEHAVEIOFFENDEDIHAVEDONENOMORETOCAESARTHANYOUSHALLDOTOBRUTUSTHEQUESTIONOFHISDEATHISENROLLEDINTHECAPITOLHISGLORYNOTEXTENUATEDWHEREINHEWASWORTHYNORHISOFFENCESENFORCEDFORWHICHHESUFFEREDDEATHHERECOMESHISBODYMOURNEDBYMARKANTONYWHOTHOUGHHEHADNOHANDINHISDEATHSHALLRECEIVETHEBENEFITOFHISDYINGAPLACEINTHECOMMONWEALTHASWHICHOFYOUSHALLNOTWITHTHISIDEPARTTHATASISLEWMYBESTLOVERFORTHEGOODOFROMEIHAVETHESAMEDAGGERFORMYSELFWHENITSHALLPLEASEMYCOUNTRYTONEEDMYDEATH

#---------------------------------------------------------------------------------------------------------------------------------
