select
    *
from upapp_user upUser
inner join upapp_userProfile upProfile on
    upUser.id = upProfile.user_id
    and upProfile.id = %s
;