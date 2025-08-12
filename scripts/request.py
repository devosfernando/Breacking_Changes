import requests
from scripts import constants


namespace = "co.cbtq.app-id-20452.pro"
#url = "https://bbva-lrba.appspot.com/gateway/ecs-live-02/lrba/v0/ns/{namespace}/status?paginationKey=0&pageSize={pagination}&jobName=&runId=&jobVersion=&status=&size=&priorityClassName=&startDate=1744088400000000000&endDate=&sort=running%2Cdesc&sort=finishDate%2Cdesc&sort=startDate%2Cdesc".format(namespace= namespace,pagination=pagination)
#https://bbva-lrba.appspot.com/gateway/ecs-live-02/lrba/v0/status?paginationKey=0&pageSize=50&jobName=&runId=&jobVersion=&status=&size=&priorityClassName=&namespace=&startDate=1744174800000000000&endDate=&sort=running%2Cdesc&sort=finishDate%2Cdesc&sort=startDate%2Cdesc
#cookie = "GCP_IAP_UID=116792461292562017642; GCP_IAP_XSRF_NONCE_vhwIu3PfwAZ0QJySwgHzsQ=1; GCP_IAP_XSRF_NONCE_ftBE1e_7jjnJptwrJHuCNw=1; __Host-GCP_IAP_AUTH_TOKEN_4230143DB71CD3D1=ASPJNyARjOInRZl5fV1DzhHYNVgn3Q601hsdzycVL3IQr0VgY399RQj9lAmHcREsTF014BwjYMRHXOfmc---0w7prkf1zjdaFw_a4C3xPm3zoUhxWAa_y6nH9y9qAR68I_cv9C-PKChZl8XQlEB6ulfVF9HgiVLo4BZSZBZUFmThzvLd1S6ac-dut5YKbO7gMCRR6T7agae69hJCnZMfKoNuPvDbqx08LZ0DQ0xrEtidzJhjzGM5fGf_m0uyvilbWhsALJeoU7gqM-0D66loqk6S3u6NAe62BqeS2diBlId8PYkVYaJkfg9gatifHkHgMVQj0fR5SCfad53ySZZCpP0j-DQTwFY7ueaQBVdcJyiiVYf-McXeSgqi_RmcLBqGW61vyYp5EeCn5TugDV0gpEGz_GCLpgm9vNNsomV969ZVDwMn8gsJ_vMGMfI_9p9inHAS1jZw03vuOiCvSdAXlbQmkBdyF-z6MR_OmP-UOggO5KRE5DL_XKgmSiQITaRtk85QepsO1VZk8buf_JHZM4fMfzEpzNT0b_twnpFx2i2QjkQjbHOI03gI2lJQ1Lxug7KweePdzOjnr_g24kOfyuFZ4IM1JxZyKLhVSypBmC-rUv7WXexujNFMphBu0cqq9EWQwjoxRabeZPDWnFsuo_BdWw3Kgbd5i97vYs3ufcuqiJ1CZ-jb417HTATcDGPre2tJlIr9MKWripYo5uAWV5YCt5krmy9RaAFmOXbR0qprrd7AKnznz5BTsUcrAp8FHTLGTbF9jEwKHjJpIZ_rpk7Cix58OPtMfdSuCoyLc-FQxojDHWkUMH5fOg2NH75FIN_actmW6DBfZH27mIYOurlHVwqi0SvYQP-Zda5FNGA8L8cwJeMTbZ0m7En2RtSSkxFNOQuEC34cWlzu603JCn5pi_uJC-FbWHcH6wztlsHul9pW4kdeydJpd_tBSL0zo_botpk7qpP4RrNSVXne2BcTbNVgvAQiCxxJiVqeAMeUoWgIo4UZoTyRyzDobT9zwjTLCVUkG6mWLMC_b7esDuB_8uh-olHexzA10rhS574f9n9b9R-Hr07BqWDXSx5wpcjPijnCOMOwnyB7v2O9xmjFt58E8bYmUGRqvN7tOliJK6xVyZScQ5Akpifh4uY0bNmdKmGwNKFa-ZJtqQNGmPosxInspx4YQ36lv4oLPTXgRGmq4kDrpo4uPMcFtWK3vr8_RrD9wNLYq9E0YTZLWc-Su8YQP1JbwuS5Ai6-2aAL4MFBhPujhPwC8_joZKzaYeeQqE9rulpzrRINbbrSLP6OyZOFPK8zZc8xvR877oIi-Hz88xtsCwGLkkH-XvUVqHNMfEM6S9jCCVDmPOn-_MMCaNDjvaEVMu6XUnJaPyjjtUebuyDpKTD3YrJ7v80-fjZRFWc8emqCtpLD-ZEJ5ye1-cXXWYfAMoVMV3vYhedda4z2hkBDJ77r8o-1MoYFyhksX3uIOuVk_ZVH9tJVz0uXM7d0chgyOnXeweRdwc5iGAdGxPnJKsU9BRA8T8HnWPlvk36aI6MA-F1ZtoUC2lueMoXL-WRt1qbsUNydoS6LdPLKw7L3lHFaXEfICR1y785ZmVG2Zw4-qYaXJNNCQCt5LkxUF9AUhI8Ewg16M9-GuLSWv3rkykX-gEUTpGyDGJVJRFedtsdJ8_kRla29qBqgfpwn-ZkAipIJAwbv50Wa3EmE816O9t0lmkB9n02NlyyhsqjdutmBl3vw4Kugc76b03r6IZYg9SbvCHOYsWVWvqVshJx-p_7buVk"
cookie = "GCP_IAP_UID=112333689722132717838; __Host-GCP_IAP_AUTH_TOKEN_4230143DB71CD3D1=ASPJNyBwBwI2URkaZEjUZk5kMNbhZ5kyp5EG8SBzhvFHFBQoIVwc2K-tlzPlw1aTQhsMIIOGNOdkTRDFivWBZeYRRKy6H_c8m0Fl_MSc8159stjBKNbHO_QkOeJpUujcGMFFjN3bYjX68KoMnDH-GWeplGWJCK30Z4zEWqSN4_qJVHMmA76FRvvrFAbLOctwGY-EYRxwiDN9Up60zKxw__jH3UwD3p0Hptgp1Dkp6QuXCBTT8pDaNLtpwwY-JnJglNcpuNQsFyt14Nw9hc2TY1bIRZ0ujrXj3qXN7Vl4YUaRBHR_eX2kG1iL4xXsGOgF9wkhzO3XGdGdnKJ-BYIw4eZhavaeMp99PNiQc4MVTZACfVs165QamrdnIE0nIOrWH2U4_b2PWvm-7znq2VlqSH4Ty9MhxNd6CkxK-ugYDjmfBdBiM73BgtrbC-rgppByx580h35VR9HGthuIvmWNsxwEYpj8CkeTzkk9afIhtK2TxJ8yEY6ljUaqNYVhBFOv_DYAcTxGA789zNcXsY0vGqUJxPW6DmULf2HjJkRuW0-bn9b_rI-ObAhMyS7xFfzzBgJw-MC93U-76PlbbnijXqXw4_7wf6RgSMGm343L1Tq6JBhJrhbx-DG4sQBakzggE4xTBycMM6hNJcc7NDZSSJhEeVP7Q973bm7_Y6oaPH01a3lS3Etm1jIDcr2i7gCs2peYwo2ChQxieJ6qn2zJWWXhye-5Rn0k0uelFYOnsKs6K2uu3OnBP0ooE_Ne7_0px-NhHzelBEWH3rEeUsdqO4zLjSqvyuWFxYyaznOkvx-pMefforR-eetaYyrvZex4KaG0s0s8WGKAZ7ipXpvrIUmGRJYsVnV97kCjuriPYR3P6VtiDud9g6RvtWZYIlOxAa24TZbG0sHjmtDvfCnZRhhr92iPEjSTZkF94KnZgheSb1RMh4L_EOKrzixZKmnHzvXTZDyDh1oEZx27_avGv4ocltj9fh_lIXtSHHekTGNXeZWq1WDx97UVZcn4RAZPXDBfB6-KeXlA_Vn5TeF0VTgUEloB8JX8JXK6jNziDp_-vS9IL_ulIIjmJCBJy0OnDGWYlTZE5nCb0kYeLnI06EOXk6XqMbp5lJxHFJN9TEFEgZ3OtHqxqPrIRWjtPDDWyIxUbgBZiJl32NqHfff7hkZ7R8Ewe9gNwyfhk_XZ2db99ZiL2L8O68nE5mW1L76NqwXr01u95wS71OIj3yRa-rmBeZFpcFDzYQVreB4sAltUSW_vfO4Ak2VtB8K4PxCzBTzm2dFI5YMC4fVG8Bk70vTYk6DAybaqVvG5JEd_onndf1HQqfkYfLHkK4OJabTKMmu54Hg-vl3u0_OnBLExoZFCj26xFWeMzPn1BMYiLN_1R0A0JlF7Iqac1KSA7TXOxxkYDzKR-YwAj50fZwljaA-Zrz0ClmFQWKpML1_YjeDkRHd8HbXQQPrGF3DUZ0OSZZfRkft4G3HHVG4Iksq7wnv02Yd_koMzWFKtDPpvGlkON6EwvmaJxj1A51-c4vpbiMBnBVB1kqp1Uyyiy8Ts-SeSv5d6gzzVZNyulQT6J_6KjaKGZyzxw1r1Nc7ixdUrjwocNw8NQi35d8fatnJEOgGMpHWtyk5TC1kKvDO9wg1vVwOb8UhvzEdhXuSARfS8TfUgCR0LsctXLO4TZi7Mh8PTaDCgeLKkebCsDM0atnoiqHbBqxNX1hHLjjKwccOw"
item = "-co-"

headers = {
    "Authorization": "Bearer",
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json",
    "Cookie": constants.COOKIE
}

def lazy_paginated_request():
    page = 50
    while True:
        pagination = "500"
        url = "https://bbva-lrba.appspot.com/gateway/ecs-live-02/lrba/v0/status?paginationKey={page}&pageSize={pagination}&jobName={item}&runId=&jobVersion=&status=SUCCESS&size=&priorityClassName=&namespace=&startDate=1733029200000000000&endDate=&sort=running%2Cdesc&sort=finishDate%2Cdesc&sort=startDate%2Cdesc".format(pagination=pagination,page=page,item=item)
        response = requests.get(url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            print("data1______111-________",data)
            pagination = data.get("pagination")
            items = data.get('result', [])
            print(items)
            if not items:
                break
            yield from items
            page += 1
            print("---------PAGE------------", page)
        else:
            print("Request failed")
            data = response.json()
            break


def create_request():
    all_results = list(lazy_paginated_request())
    print("Total:", len(all_results))
    return all_results
