alter table upapp_projectfunction
rename column "functionName" to name;

alter table upapp_projectfunction
rename to upapp_role;

drop table "upapp_candidateinterest_currentSkills";

drop table "upapp_candidateinterest_interestedFunctions";

alter table upapp_project
rename column "function_id" to role_id;