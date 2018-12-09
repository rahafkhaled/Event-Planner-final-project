import string
def venue(s):
        message="hotel:usrname:rahaf:date:7/3/2019:time:7.30pm:type:Ballroom:capacity:700"
        #message decoded
        username2=message[14:]
        findColonBeforeDate=username2.find(":")
        actualUsername=username2[:findColonBeforeDate]
        date2=username2[findColonBeforeDate+6:]
        findColonBeforeTime=date2.find(":")
        actualDate=date2[:findColonBeforeTime]
        time2=date2[findColonBeforeTime+6:]
        findColonBeforeType=time2.find(":")
        actualTime=time2[:findColonBeforeType]
        type2=time2[findColonBeforeType+6:]
        findColonBeforeCapacity=type2.find(":")
        actualType=type2[:findColonBeforeCapacity]
        actualCapacity=type2[findColonBeforeCapacity+10:]
        mList=[actualUsername,actualType,actualDate,actualTime,actualCapacity]
        mString="-".join(mList)
        print mString
        print mString.split("-")
     
##        findColonBeforeRating=venue1.find(":")
##        actualType=venue1[:findColonBeforeRating]
##        rating1=venue1[len(actualType)+8:]
##        findColonBeforeLocation=rating1.find(":")
##        actualRating=rating1[:findColonBeforeLocation]
##        location1=rating1[len(actualRating)+10:]
##        findColonBeforeBudget=location1.find(":")
##        actualLocation=location1[:findColonBeforeBudget]
##        budget1=location1[len(actualLocation)+8:]
##        findColonBeforeCapacity=budget1.find(":")
##        actualBudget=budget1[:findColonBeforeCapacity]
##        actualCapacity=budget1[len(actualBudget)+10:]


venue(958)
