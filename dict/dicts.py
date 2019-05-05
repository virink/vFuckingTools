def ssrf():
    dicts = load_dict('./../vFuckingTools/dict/ssrf/ssrf.dic')
    for i in dicts:
        fn = i.replace('\n', '')
