--@exclude_input=o2o_ad.dwd_tag_taobao_id_oneid_df
--@extra_output=dws_tb_o2obh_user_inter_action_di_u_c_trd
--@exclude_output=dws_tb_o2obh_user_inter_action_di 
--odps sql 
--********************************************************************--
--author:谦诚
--create time:2019-10-21
--********************************************************************--
INSERT OVERWRITE TABLE dws_tb_o2obh_user_inter_action_di PARTITION(ds='${bizdate}',action='u_c_trd')
SELECT  oneid
        ,user_id
        ,NULL
        ,NULL
        ,NULL
        ,NULL
        ,NULL
        ,NULL
        ,NULL
        ,NULL
        ,category_id
        ,'cat_leaf' as object_type
        ,trade_cnt as action_cnt
		,NULL AS addition_indexs
        ,total_trade_amt
        ,NULL AS user_real_pay_amt
        ,NULL AS shop_real_receive_amt
        ,NULL AS total_voucher_cnt
        ,NULL AS merchant_subsidy_amt
        ,NULL AS platform_subsidy_amt
        ,action_item_qty
FROM    (
            SELECT  user_id
                    ,category_id
                    ,SUM(COUNT) as trade_cnt
                    ,SUM(amount) as total_trade_amt
                    ,COUNT(1) as action_item_qty
            FROM    o2o_ad.ads_algo_portrait_tb_user_buy_item_ds
            WHERE   ds = '${bizdate}'
            GROUP BY user_id
                     ,category_id
        ) as t1
LEFT OUTER JOIN (
                    SELECT  taobao_id
					,oneid
					,score
					FROM    o2o_ad.dwd_tag_taobao_id_oneid_mapping_df
					WHERE   ds = MAX_PT('o2o_ad.dwd_tag_taobao_id_oneid_mapping_df')
                ) as t2
ON      t1.user_id = t2.taobao_id
;