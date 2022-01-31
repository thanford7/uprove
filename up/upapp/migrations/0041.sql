alter table upapp_skill
add column "isRequired" boolean NOT NULL default false,
add column "isRecommended" boolean NOT NULL default true,
add column "skillLevelBits" smallint NULL,
add column "skillProject_id" bigint NULL
;

alter table upapp_skill
drop constraint "upapp_projectskill_skillName_key";

ALTER TABLE "upapp_skill" ADD CONSTRAINT "upapp_skill_skillProject_id_e5add92c_fk_upapp_project_id" FOREIGN KEY ("skillProject_id") REFERENCES "upapp_project" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "upapp_skill_skillProject_id_e5add92c" ON "upapp_skill" ("skillProject_id");