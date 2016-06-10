# coding=utf-8

_IP = "([0-9]{1,3})(\\.[0-9]{1,3}){3}"
_STR = "([A-Z|a-z]+[0-9]*)"
_Sn = _IP + "_(java|python|cpp)" + "(:([A-Z|a-z]+[0-9]*)){2}"


class Regex(object):
    # Routing statement. Examples:
    #
    # S1 + S2 + S3;
    #
    # S1 , S2 + S3;
    #
    # S1 + S2 , S3;
    #
    # S1 , S2 + &S3;
    #
    # S1;
    #
    # Note that regular expression does not include end of statement operator.
    ROUTING_STATEMENT = _Sn + "(," + _Sn + ")*" + "((\\+&?" + _Sn +\
                        ")*|(\\+" + _Sn + "(," + _Sn + ")*)*)"

    # CLARA simple Condition.Example:
    # Service == "state_name"
    # Service != "state_name"
    SIMPLE_CONDITION = _Sn + "(==|!=)\"" + _STR + "\""

    # CLARA complex Condition.Example:
    # (S1 == "state_name1" && S2 == "state_name2) {
    # S1 == "state_name1" !! S2 == "state_name2" !! S2 != "state_name3") {
    COMPLEX_CONDITION = SIMPLE_CONDITION + "((&&|!!)" + SIMPLE_CONDITION + ")*"

    # CLARA conditional statement
    CONDITION = "((\\}?if|\\}elseif)\\(" + COMPLEX_CONDITION + "\\)\\{" +\
                ROUTING_STATEMENT + ")|(\\}else\\{" + ROUTING_STATEMENT + ")"
