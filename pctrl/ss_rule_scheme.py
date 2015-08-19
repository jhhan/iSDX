#  Author:
#  Rudiger Birkner (Networked Systems Group ETH Zurich)


import ss_lib

LOG = True

# PRIORITIES (Values can be in [0,65535], 0 is miss)
FLOW_MISS_PRIORITY = 0


# outbound switch priorities
OUTBOUND_HIT_PRIORITY = 1

# inbound switch priorities
INBOUND_HIT_PRIORITY = 2
INBOUND_MISS_PRIORITY = 1



# create new outbound rules in response to superset changes
def update_outbound_rules(sdx_msgs, policies, supersets, my_mac):
    dp_msgs = {"type": "add",
                    "changes": []}

    if 'outbound' not in policies:
        return dp_msgs

    outbound = policies['outbound']

    # map each participant to a list of our policies which forward to them
    part_2_policy = {}

    # build this mapping
    for policy in outbound:
        if "fwd" in policy["action"]:
            part = policy["action"]["fwd"]
            if part not in part_2_policy:
                part_2_policy[part] = []
            part_2_policy[part].append(policy)


    # if the supersets needed to be recomputed
    if sdx_msgs["type"] == "new":
        dp_msgs["type"] = "new"

    updates = sdx_msgs["changes"]
    for update in updates:
        participant_id = update["participant_id"]
        superset_id = update["superset"]
        bit_position = update["position"]

        if participant_id not in part_2_policy:
            continue

        for policy in part_2_policy[participant_id]:
            vmac = vmac_participant_match(superset_id, participant_index, supersets):
            vmac_bitmask = vmac_participant_mask(participant_index, supersets)

            next_hop_mac = vmac_next_hop_match(participant_name, supersets, inbound_bit = True)

            match_args = policy["match"]
            match_args["eth_dst"] = (vmac, vmac_bitmask)
            match_args["eth_src"] = my_mac

            actions = {"set_eth_dst":next_hop_mac, "fwd":"inbound"}

            rule = {"rule_type":"outbound", "priority":OUTBOUND_HIT_PRIORITY,
                    "match":match_args , "action":actions, "mod_type":"insert"}

            dp_msgs["changes"].append(rule)






def build_outbound_rules_for(out_policies, ss_instance, my_mac):
    "Given a subset of outbound policies, return all the resulting rules."

    rules = []

    part_2_superset = {}
    for ss_id, superset in enumerate(ss_instance.supersets):
        for part_index, part in enumerate(superset):

            if part not in part_2_superset:
                part_2_superset[part] = []

            part_2_superset.append((ss_id, part_index))


    for policy in out_policies:
        if "fwd" not in policy["action"]:
            continue

        part = policy["action"]["fwd"]

        for ss_id, part_index in part_2_superset[part]:
            vmac = vmac_participant_match(ss_id, 
                            part_index, ss_instance)
            vmac_bitmask = vmac_participant_mask(part_index, ss_instance)

            match_args = policy["match"]
            match_args["eth_dst"] = (vmac, vmac_bitmask)
            match_args["eth_src"] = my_mac

            actions = {"set_eth_dst":next_hop_mac, "fwd":"inbound"}

            rule = {"rule_type":"outbound", "priority":OUTBOUND_HIT_PRIORITY,
                    "match":match_args , "action":actions, "mod_type":"insert"}

            rules.append(rule)

        return rules


def build_inbound_rules_for(participant_id, in_policies, supersets, port_count):
    "Given a subset of inbound policies, return all the resulting rules."

    rules = []


    for policy in in_policies:
        if "fwd" not in policy["action"]:
            continue

        port_num = policy["action"]["fwd"]

        # match on the next-hop
        vmac_bitmask = vmac_next_hop_mask(supersets)
        vmac = vmac_next_hop_match(participant_id, supersets)


        match_args = policy["match"]
        match_args["eth_dst"] = (vmac, vmac_bitmask)


        port_num = policy["action"]["fwd"]
        if (port_num >= port_count):
            port_num = 0
        new_vmac = vmac_part_port_match(participant_id, port_num, supersets)                

                    
        actions = {"set_eth_dst":new_vmac, "fwd":"main"}

        rule = {"rule_type":"inbound", "priority":INBOUND_HIT_PRIORITY,
                "match":match_args, "action":actions, "mod_type":"insert"}

        rules.append(rule)

    return dp_msgs








# initialize all inbound rules
def init_inbound_rules(participant_id, policies, supersets, port_count):
    dp_msgs = {"type": "new",
                    "changes": []}


    if LOG:
        self.logger.info("INIT: -- Installing inbound switch rules --")


    # do we even have inbound policies?
    if ('inbound' not in policies):
        return None

    in_policies = policies['inbound']

    rules = build_inbound_rules_for(participant_id, in_policies, supersets, port_count)

    dp_msgs["changes"] = rules

    return dp_msgs

    




