#!/usr/bin/env python3

import regex

#regex to search for urls with paramters
params = r"(\?|&)([^=]+)="

#test string
test = "https://www.example.com/?test=1&test2=2&test3=3"
test1 = "https://www.example.com/?test=1&test2=2&test3=3&test4=4"
test2 = "https://www.example.com/?test=1&test2=2&test3=3&test4=4&test5=5"
test3 = "https://www.example.com/?test=1&test2=2&test3=3&test4=4&test5=5&test6=6"
test_no_params = "https://www.example.com/"
test_no_params2 = "https://www.example.com/google&2/3/gmail.com"
test_4 = "https://www.google.com/%22';cWc(c,SKc(d));c.a+='/%22"
test_5 = "https://www.google.com/%22/ads/publisher/partners/static/images/menu.svg/%22"
test_6 = "http://www.google.com/%22;cWc(c,SKc(a.a));c.a+=/%22"
test_7 ="https://www.google.com/%22https://accounts.google.com/ServiceLogin?service=searchandassistant&passive=1209600&continue=https://www.google.com/travel/hotels/Abuja/entity/CgsI34SWmIjp8M2jARABGn5BSDNoLWpTQmVZaGtoam1UM1MxNjBDTHdLZ2tWY190V2M2bWU1N1ZWZGNNZlVZLUNwc2tJYUVtYktxaVZ1ekZqdWNyay1LX2lmTXQ0WkpXSW4wY1BTcWQ5MkQtZFNOQ2pNODJVYlZPTS1HZFRHZ2R0aWpVV1E3ZWdmTlFHcnc?q%3Dlist%2Bof%2Bhotels%2Bin%2Babuja%2Band%2Btheir%2Baddresses%26g2lb%3D2502548,2503771,2503781,4258168,4270442,4284970,4291517,4306835,4597339,4718358,4723331,4731329,4757164,4814050,4816977,4821091,4852066,4861688,4864715,4878644,4885165,4886480,4887074,4887844,4891509,4892549,4892563,4892565,4893075%26hl%3Den-NG%26gl%3Dng%26ssta%3D1%26ts%3DCAESABopCgsSBzoFQWJ1amEaABIaEhQKBwjmDxAMGAQSBwjmDxAMGAUYATICEAAqCQoFOgNOR04aAA%26rp%3DEN_L3Yrwrofd9wEQhOqFxMjArv2cARDhnf7yiMb0yysQwYH8j8fP-ZImogEFQWJ1amE4AUAASAKKAitsaXN0IG9mIGhvdGVscyBpbiBhYnVqYSBhbmQgdGhlaXIgYWRkcmVzc2VzmgICCAA%26ap%3DEgNDQmcwA2gB%26ictx%3D1%26sa%3DX%26ved%3D0CAAQ5JsGahcKEwiwqLGB8pf7AhUAAAAAHQAAAAAQBA%26utm_campaign%3Dsharing%26utm_medium%3Dlink%26utm_source%3Dhtls&followup=https://www.google.com/travel/hotels/Abuja/entity/CgsI34SWmIjp8M2jARABGn5BSDNoLWpTQmVZaGtoam1UM1MxNjBDTHdLZ2tWY190V2M2bWU1N1ZWZGNNZlVZLUNwc2tJYUVtYktxaVZ1ekZqdWNyay1LX2lmTXQ0WkpXSW4wY1BTcWQ5MkQtZFNOQ2pNODJVYlZPTS1HZFRHZ2R0aWpVV1E3ZWdmTlFHcnc?q%3Dlist%2Bof%2Bhotels%2Bin%2Babuja%2Band%2Btheir%2Baddresses%26g2lb%3D2502548,2503771,2503781,4258168,4270442,4284970,4291517,4306835,4597339,4718358,4723331,4731329,4757164,4814050,4816977,4821091,4852066,4861688,4864715,4878644,4885165,4886480,4887074,4887844,4891509,4892549,4892563,4892565,4893075%26hl%3Den-NG%26gl%3Dng%26ssta%3D1%26ts%3DCAESABopCgsSBzoFQWJ1amEaABIaEhQKBwjmDxAMGAQSBwjmDxAMGAUYATICEAAqCQoFOgNOR04aAA%26rp%3DEN_L3Yrwrofd9wEQhOqFxMjArv2cARDhnf7yiMb0yysQwYH8j8fP-ZImogEFQWJ1amE4AUAASAKKAitsaXN0IG9mIGhvdGVscyBpbiBhYnVqYSBhbmQgdGhlaXIgYWRkcmVzc2VzmgICCAA%26ap%3DEgNDQmcwA2gB%26ictx%3D1%26sa%3DX%26ved%3D0CAAQ5JsGahcKEwiwqLGB8pf7AhUAAAAAHQAAAAAQBA%26utm_campaign%3Dsharing%26utm_medium%3Dlink%26utm_s"
test_8 = "https://www.google.com/%22https://accounts.google.com/ServiceLogin?service=searchandassistant&passive=1209600&continue=https://www.google.com/travel/hotels/Abuja/entity/CgoI5bvYnaHz7tEKEAEafkFBcFB3T2xYSGVmMVNnaGNDem13dFQzZ2NsMlA5bGZBZ1dMZXRld21ycGhSWWV3OHpUeVF1VGlIV3l5c012OHRVSUpHUElRRTUyWGdkQnJtcXBfNVc2bVRUem5VUWJraG1OTlFCMm16TjhicUwzdm1nYTZhbDRBRk5zZkJGdw?q%3Dlist%2Bof%2Bhotels%2Bin%2Babuja%2Band%2Btheir%2Baddresses%26g2lb%3D2502548,2503771,2503781,4258168,4270442,4284970,4291517,4306835,4597339,4718358,4723331,4731329,4757164,4814050,4816977,4821091,4852066,4861688,4864715,4878644,4885165,4886480,4887074,4887844,4891509,4892549,4892563,4892565,4893075%26hl%3Den-NG%26gl%3Dng%26ssta%3D1%26ts%3DCAESABopCgsSBzoFQWJ1amEaABIaEhQKBwjmDxAMGAQSBwjmDxAMGAUYATICEAAqCQoFOgNOR04aAA%26rp%3DEN_L3Yrwrofd9wEQhOqFxMjArv2cARDhnf7yiMb0yysQwYH8j8fP-ZImogEFQWJ1amE4AUAASAKKAitsaXN0IG9mIGhvdGVscyBpbiBhYnVqYSBhbmQgdGhlaXIgYWRkcmVzc2VzmgICCAA%26ap%3DEgNDQXcwA2gB%26ictx%3D1%26sa%3DX%26ved%3D0CAAQ5JsGahcKEwiQ9IHb2pf7AhUAAAAAHQAAAAAQAw%26utm_campaign%3Dsharing%26utm_medium%3Dlink%26utm_source%3Dhtls&followup=https://www.google.com/travel/hotels/Abuja/entity/CgoI5bvYnaHz7tEKEAEafkFBcFB3T2xYSGVmMVNnaGNDem13dFQzZ2NsMlA5bGZBZ1dMZXRld21ycGhSWWV3OHpUeVF1VGlIV3l5c012OHRVSUpHUElRRTUyWGdkQnJtcXBfNVc2bVRUem5VUWJraG1OTlFCMm16TjhicUwzdm1nYTZhbDRBRk5zZkJGdw?q%3Dlist%2Bof%2Bhotels%2Bin%2Babuja%2Band%2Btheir%2Baddresses%26g2lb%3D2502548,2503771,2503781,4258168,4270442,4284970,4291517,4306835,4597339,4718358,4723331,4731329,4757164,4814050,4816977,4821091,4852066,4861688,4864715,4878644,4885165,4886480,4887074,4887844,4891509,4892549,4892563,4892565,4893075%26hl%3Den-NG%26gl%3Dng%26ssta%3D1%26ts%3DCAESABopCgsSBzoFQWJ1amEaABIaEhQKBwjmDxAMGAQSBwjmDxAMGAUYATICEAAqCQoFOgNOR04aAA%26rp%3DEN_L3Yrwrofd9wEQhOqFxMjArv2cARDhnf7yiMb0yysQwYH8j8fP-ZImogEFQWJ1amE4AUAASAKKAitsaXN0IG9mIGhvdGVscyBpbiBhYnVqYSBhbmQgdGhlaXIgYWRkcmVzc2VzmgICCAA%26ap%3DEgNDQXcwA2gB%26ictx%3D1%26sa%3DX%26ved%3D0CAAQ5JsGahcKEwiQ9IHb2pf7AhUAAAAAHQAAAAAQAw%26utm_campaign%3Dsharing%26utm_medium%3Dlink%26utm_sou"
test_9  ="https://www.google.com/%22https://lh3.googleusercontent.com/-U8cX3to_VdQsSRJZmkhby92ajzaIOaUk91RGpoFZpASE_QalkZUbgwMippJxtKEREgx1EWxtSU0IOC6hW8LxlDwqhPER9jaF8tXKi8=h100/%22/n"
test_10 = "https://www.google.com/%22https://lh3.googleusercontent.com/-U8cX3to_VdQsSRJZmkhby92ajzaIOaUk91RGpoFZpASE_QalkZUbgwMippJxtKEREgx1EWxtSU0IOC6hW8LxlDwqhPER9jaF8tXKi8=h52/%22/n"
test_11 = "https://www.google.com/%22https://lh3.googleusercontent.com/-U8cX3to_VdQsSRJZmkhby92ajzaIOaUk91RGpoFZpASE_QalkZUbgwMippJxtKEREgx1EWxtSU0IOC6hW8LxlDwqhPER9jaF8tXKi8=h57/%22/n"
test_12 = "https://www.google.com/%22https://lh3.googleusercontent.com/26tfwfFQ0J4N4ErSwZWOTkFQv5m99t1ObE26jSFfp10OXv6YJb6U8apZjHwKezPnQgKjbzKRn4Q1ybzRaiqMuWDm1s2ttoy-dGkfkg=h100/%22/n"
test_13 ="https://www.google.com/%22https://lh3.googleusercontent.com/26tfwfFQ0J4N4ErSwZWOTkFQv5m99t1ObE26jSFfp10OXv6YJb6U8apZjHwKezPnQgKjbzKRn4Q1ybzRaiqMuWDm1s2ttoy-dGkfkg=h52/%22/n"

list_urls = [test, test1, test2, test3, test_no_params, test_no_params2, test_4, test_5, test_6, test_7, test_8, test_9, test_10, test_11, test_12, test_13]


all_params_uris = [url for url in list_urls if regex.search(params, url)]

final_uris = []
for uri in all_params_uris:
    delim = uri.find("=") + 1
    final_uri = uri[:delim] + 'FUZZ'
    final_uris.append(final_uri)

print(final_uris)
    


