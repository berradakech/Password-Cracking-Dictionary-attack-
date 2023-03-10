import itertools
import hashlib
import time

# all the possible characters
chars = "abcdefghijklmnopqrstuvwxyz1234567890"
# all the hashes
hashes = set([
    "7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5",
    "37a2b469df9fc4d31f35f26ddc1168fe03f2361e329d92f4f2ef04af09741fb9",
    "19dbaf86488ec08ba7a824b33571ce427e318d14fc84d3d764bd21ecb29c34ca",
    "06240d77c297bb8bd727d5538a9121039911467c8bb871a935c84a5cfe8291e4",
    "f5cd3218d18978d6e5ef95dd8c2088b7cde533c217cfef4850dd4b6fa0deef72",
    "dd9ad1f17965325e4e5de2656152e8a5fce92b1c175947b485833cde0c824d64",
    "845e7c74bc1b5532fe05a1e682b9781e273498af73f401a099d324fa99121c99",
    "a6fb7de5b5e11b29bc232c5b5cd3044ca4b70f2cf421dc02b5798a7f68fc0523",
    "1035f3e1491315d6eaf53f7e9fecf3b81e00139df2720ae361868c609815039c",
    "10dccbaff60f7c6c0217692ad978b52bf036caf81bfcd90bfc9c0552181da85a"
])

begin = time.time()
for length in range(4, 7):
    for comb in itertools.product(chars, repeat=length):
        # from "('a', 'a', 'a', 'a')" to 'aaaa'
        password = "".join(comb)
        # compute the hash
        h = hashlib.sha256(password.encode())
        digest = h.hexdigest()
        if digest in hashes:
            # if one hash match, print and remove (to save some time)
            print("{} === {}".format(digest, password))
            hashes.remove(digest)
        else:
            # print your progress
            print(password, end="\r")

end = time.time()
print("Time for naïve: {:.3f}".format(end - begin))

