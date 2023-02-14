import hashlib
import itertools
import multiprocessing

all_hashes = {"7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5",
              "37a2b469df9fc4d31f35f26ddc1168fe03f2361e329d92f4f2ef04af09741fb9",
              "19dbaf86488ec08ba7a824b33571ce427e318d14fc84d3d764bd21ecb29c34ca",
              "06240d77c297bb8bd727d5538a9121039911467c8bb871a935c84a5cfe8291e4",
              "f5cd3218d18978d6e5ef95dd8c2088b7cde533c217cfef4850dd4b6fa0deef72",
              "dd9ad1f17965325e4e5de2656152e8a5fce92b1c175947b485833cde0c824d64",
              "845e7c74bc1b5532fe05a1e682b9781e273498af73f401a099d324fa99121c99",
              "a6fb7de5b5e11b29bc232c5b5cd3044ca4b70f2cf421dc02b5798a7f68fc0523",
              "1035f3e1491315d6eaf53f7e9fecf3b81e00139df2720ae361868c609815039c",
              "10dccbaff60f7c6c0217692ad978b52bf036caf81bfcd90bfc9c0552181da85a"}


def modif1(p: str):
    return p.title()


def modif2(p: str):
    return p.replace("e", "3")


def modif3(p: str):
    return p.replace("o", "0")


def modif4(p: str):
    return p.replace("i", "1")


def modif_and_hash(p):
    "Try all modifications and hashes from one given base password."
    if len(all_hashes) == 0:
        return
    p = p.replace("\n", "")  # ensure there are no \n at the end

    # create the alternative from the base passwords
    all_versions = set([p])  # include the base password for comb in all_modifs_combinations:
    for comb in all_modifs_combinations:
        p_temp = p
        for modificator in comb:
            p_temp = modificator(p_temp)
        all_versions.add(p_temp)
        # Hash and compare each of them
    for version in all_versions:
        hash = hashlib.sha256(version.encode()).hexdigest()
        if hash in all_hashes:
            print("{} === {} (from {})".format(hash, version, p))
            all_hashes.remove(hash)
            return p, hash


# define the name of all dictionaries, along with their encoding
dictionaries = [
    ("500-worst-passwords.txt", "utf-8"),
    ("alypaa.txt", "utf-8"),
    ("cain.txt", "utf-8"),
    ("carders.cc.txt", "latin-1"),
    ("conficker.txt", "utf-8"),
    ("english.txt", "utf-8"),
    ("elitehacker.txt", "utf-8"),
    ("facebook-pastebay.txt", "utf-8"),
    ("facebook-phished.txt", "latin-1"),
    ("faithwriters.txt", "utf-8"),
    ("file-locations.txt", "utf-8"),
    ("fuzzing-strings.txt", "utf-8"),
    ("german.txt", "latin-1"),
    ("hak5.txt", "utf-8"),
    ("honeynet.txt", "latin-1"),
    ("hotmail.txt", "utf-8"),
    ("john.txt", "utf-8"),
    ("phpbb.txt", "latin-1"),
    ("phpmyadmin-locations.txt", "latin-1"),
    ("singles.org.txt", "utf-8"),
    ("tuscl.txt", "latin-1"),
    ("twitter-banned.txt", "utf-8"),
    ("us_cities.txt", "utf-8"),
    ("web-extensions.txt", "utf-8"),
    ("web-mutations.txt", "utf-8"),
    ("rockyou.txt", "latin-1"),
    ("crackstation.txt", "latin-1")
]

all_modifs_combinations = set()
all_modifs = [modif1, modif2, modif3, modif4]
for length in range(1, len(all_modifs) + 1):
    for comb in itertools.permutations(all_modifs, length):
        all_modifs_combinations.add(comb)

# iterate through all dictionaries
for fname, encoding in dictionaries:
    print("Opening file {}".format(fname))
    file = open("Dictionaries/{}".format(fname), encoding=encoding)
    pool = multiprocessing.Pool(8) # define a pool of 8 workers
    results = []

# read the file by chunks of 10k rows at a time, then feed one
# rows one after the other to a worker
for r in pool.imap_unordered(modif_and_hash, file, 10000):
    if r is not None:
        results.append(r)
file.close()