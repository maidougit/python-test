
from com.maimai.python.np.CF.recall_path1.load_data import create_user_item_click
from com.maimai.python.np.CF.recall_path1.base import cal_allSim
import time
import numpy as np
############################3.1预测评分
def predict_score_baseUser(uid,iid,user_item,sim_dict):
    #拿出相似用户 top30
    user_sim=dict(sorted(sim_dict[uid].items(),key=lambda x:x[1],reverse=True)[:100])

    temp1=0
    temp2=0

    #1.遍历新相似uid的other_Uid和score
    for other_user_id,sim in user_sim.items():
        if user_item[other_user_id].get(iid,-1)==-1:
            continue
        else:
            score=user_item[other_user_id][iid]
            temp1+=score*user_sim[other_user_id]
            temp2+=user_sim[other_user_id]

    if temp2==0:
        return 0
    sims=np.around(temp1/temp2,2)
    # print("用户-%s对物品-%s的预测评分为%f" % (uid,iid,sims ))
    return sims
def predict_all_score_baseUser(uid,user_item,item_set,sim_dict,top_item=100):
    """
    :param uid: 用户id
    :param user_item: 用户_物品词典
    :param item_set: 物品列表
    :param sim_dict: 用户相似词典
    :param top_item: 最相似的topk个物品推荐
    :return:
    """
    un_score_item=item_set-set(user_item[uid].keys())
    rec_item_dict={}
    for iid in un_score_item:
        s=predict_score_baseUser(uid, iid, user_item, sim_dict)
        rec_item_dict[iid]=s
        print("用户:%s 对物品:%s 的预测评分为%f" % (uid, iid, rec_item_dict[iid]))

    res=dict(sorted(rec_item_dict.items(),key=lambda x:x[1],reverse=True)[:top_item])
    print(res)
    return res
############################3.2隐式预测
def predict_click_baseUser(uid,user_item,sim_dict,top_item=200):
    #1.用户浏览过的物品
    uid_item=user_item[uid]
    #2.对相似用户进行排序
    uid_sim_otherid=sorted(sim_dict[uid].items(),key=lambda x:x[1],reverse=True)
    #2.找出用户的相似物品
    rec_item=set()

    for uid,value in uid_sim_otherid:
        item_set=set(user_item[uid])-uid_item
        rec_item=rec_item | item_set
        if len(rec_item)>top_item:
            return rec_item

if __name__ == '__main__':
    path='../data/ua.base'
    # step1 获取user_item的用户 物品词典 离线加载好的 算一次就好
    user_item=create_user_item_click(path)
    # print(user_item)

    #step2 计算用户相似矩阵（词典） 离线加载好的算一次就好

    sim_dict=cal_allSim(user_item,method="jaccard")

    #序列化

    # with open() :

    #step3 多次请求


    start=time.time()

    item_list=predict_click_baseUser("1",user_item,sim_dict,top_item=200)

    end = time.time()
    print(item_list)
    print(end-start)

