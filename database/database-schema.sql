CREATE TABLE IF NOT EXISTS "job_table"(
    "job_id" UUID NOT NULL,
    "username" TEXT NOT NULL,
    "flow_source" TEXT NOT NULL,
    "input_folder" TEXT NOT NULL,
    "output_folder" TEXT NOT NULL,
    "running_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "status" TEXT NOT NULL,
    "tags" TEXT NULL,
    "pipeline" TEXT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "end_time" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE
    "job_table" ADD PRIMARY KEY("job_id");

CREATE TABLE "review_status_table"(
    "job_id" UUID NOT NULL,
    "review_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "dur_await_review" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "in_review" BOOLEAN NOT NULL
);
ALTER TABLE
    "review_status_table" ADD PRIMARY KEY("job_id");
CREATE TABLE "record_table"(
    "record_id" UUID NOT NULL,
    "job_id" UUID NOT NULL,
    "output_file_path" TEXT NOT NULL,
    "record_index" INTEGER NOT NULL,
    "file_name" TEXT NOT NULL,
    "document_path" TEXT NOT NULL,
    "error_message" TEXT NOT NULL,
    "error_type" TEXT NOT NULL,
    "step_name" TEXT NOT NULL
);
ALTER TABLE
    "record_table" ADD PRIMARY KEY("record_id");
CREATE TABLE "record_values"(
    "key_id" UUID NOT NULL,
    "record_id" UUID NOT NULL,
    "job_id" UUID NOT NULL,
    "key" TEXT NOT NULL,
    "value" TEXT NOT NULL,
    "error_msg" TEXT NOT NULL
);
ALTER TABLE
    "record_values" ADD PRIMARY KEY("key_id");
ALTER TABLE
    "record_values" ADD CONSTRAINT "record_values_job_id_foreign" FOREIGN KEY("job_id") REFERENCES "job_table"("job_id");
ALTER TABLE
    "record_values" ADD CONSTRAINT "record_values_record_id_foreign" FOREIGN KEY("record_id") REFERENCES "record_table"("record_id");
ALTER TABLE
    "record_table" ADD CONSTRAINT "record_table_job_id_foreign" FOREIGN KEY("job_id") REFERENCES "job_table"("job_id");