from random import randint
from secrets import randbelow

# from time import sleep


def luhn(n):
    r = [int(ch) for ch in str(n)][::-1]
    # print(r)
    # print(r[0::2])
    # print(r[1::2])
    return (sum(r[0::2]) + sum(sum(divmod(d * 2, 10)) for d in r[1::2])) % 10 == 0


def gen_chk(cc):
    chk = cc[1::2]
    # print(chk)
    for i in range(len(chk)):
        n = chk[i] * 2
        if n <= 9:
            chk[i] = n
        else:
            chk[i] = n - 9
    # print(chk)
    # print(cc[0::2])
    lc = (sum(chk) + sum(cc[0::2])) * 9
    # print(lc)
    lc = int(str(lc)[-1])
    cc.append(lc)
    return cc


def gen_infos(cc):
    if int(cc[0]) == 3:
        cvv = 0
        while cvv < 100:
            cvv = randbelow(9999)
        if cvv < 1000:
            cvv = "0" + str(cvv)

    else:
        cvv = 0
        while cvv < 10:
            cvv = randbelow(999)
        if cvv < 100:
            cvv = "0" + str(cvv)
        cvv = str(cvv)
    month = str(randint(1, 12))
    if int(month) < 10:
        month = "0" + month
    return month, str(randint(2020, 2025)), str(cvv)


def gen_cc(bin=None, month=None, year=None, cvv=None, num=None):
    if num is None:
        num = 10
    try:
        if int(month) < 10:
            month = "0" + str(month)
    except Exception as e:
        pass

    # print(f'{bin}  {num} {len(bin)}')
    bin = str(bin.strip())
    rn = 15 if int(bin[0]) == 3 else 16
    # print(rn)
    for i in range(rn - len(bin)):
        bin += "x"
    # print(len(bin))
    if len(bin) in [15, 16]:
        # print('enter')
        try:
            int(bin[-1])
            gen = False

        except Exception as e:

            gen = True
            # print(gen)
            bin = bin[:-1]
            # print(len(bin))

    gen_ccs = []
    full_gen_ccs = []
    # print(bin)
    count = 1
    while True:
        cc = []
        for ch in bin:
            try:
                cc.append(int(ch))
            except Exception as e:
                cc.append(randbelow(10))
        # print(gen)
        try:
            if gen:
                cc = gen_chk(cc)
        except Exception as e:
            break

        scc = ""
        for i in cc:
            scc = scc + str(i)
        c = luhn(scc)
        # print(c)
        # sleep(2)
        m, y, gc = gen_infos(scc)

        infos = "|"
        try:

            infos = (
                infos + str(m if month is None or 12 < int(month) < 1 else month) + "|"
            )
        except Exception as e:
            infos + str(m)
        try:
            infos = infos + str(y if year is None or int(year) < 20 else year) + "|"
        except Exception as e:
            infos + str(y)
        cl = 4 if int(scc[0]) == 3 else 3
        try:
            infos = infos + str(gc if cvv is None or len(str(cvv)) != cl else cvv)
        except Exception as e:
            infos = infos + gc

        if c and (scc not in gen_ccs):
            gen_ccs.append(scc)
            scc = scc + infos
            full_gen_ccs.append(scc)
            # print(scc)
            count += 1
            # print(count)
        if count > num:
            break
    # print(len(full_gen_ccs))
    return full_gen_ccs


if __name__ == "__main__":
    # pass

    # bn = "3750984xx5x3005"0
    # bn = '375987xxxxxx00x'

    # cards_infos = []
    cards = []
    bins = [
        "484431",
        "465901",
        "475714",
        "475117",
        "465859",
        "545140",
        "475111",
        "475130",
        "492915",
        "475129",
        "446292",
        "475128",
        "484431",
        "456726",
        "476223",
        "465902",
        "475116",
    ]
    # cards = gen_cc(bn, 100)
    # 376456787931005
    # 379052xxxxxx00x

    bn = "37479000138x00x"

    # for i in range(10):
    #     n_bn = bn + str(i) + '00x'
    #     cards = gen_cc(n_bn, 10)
    #     for c in cards:
    #         print(c)
    # print('\n')

    # cards = gen_cc(bn, month=11, year=2024, cvv='7609', num=100)
    cards = gen_cc(bn, num=20)
    for c in cards:
        print(c)
