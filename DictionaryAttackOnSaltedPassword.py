import hashlib
import itertools
import multiprocessing

all_hashes_c = {"7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5",
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


def salt_and_hash(p):
    """Take one password, and hash it using all the possible salts."""
    salts = ["b9", "be", "bc", "72", "9f", "17", "94", "7f", "2e", "24"]
    p = p.replace("\n", "")  # remove possible trailing \n
    for s in salts:
        salted = p + s
        hash = hashlib.sha256(salted.encode()).hexdigest()
        if hash in all_hashes_c:
            print("{} === {} (salt {})".format(hash, p, s))
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

# try multiple files
for fname, encoding in dictionaries:
    print("Opening file {}".format(fname))
    file = open("Dictionaries/{}".format(fname), encoding=encoding)
    pool = multiprocessing.Pool(8)  # 8 concurrent workers
    results = []
    # open the file 10k rows at a time, and feed them to "salt_and_hash"
    for r in pool.imap_unordered(salt_and_hash, file, 10000):
        # store your results, for later use
        if r is not None:
            results.append(r)
    file.close()
