# Generated by Django 3.2.9 on 2022-01-25 17:28

from django.db import migrations, transaction


def populate_wait_resume_on_expire(apps, schema_editor):
    FlowSession = apps.get_model("flows", "FlowSession")
    FlowRun = apps.get_model("flows", "FlowRun")

    num_updated = 0

    while True:
        with transaction.atomic():
            # get a batch of sessions which don't have wait_resume_on_expire set
            batch = list(FlowSession.objects.filter(wait_resume_on_expire__isnull=True).only("id", "status")[:1000])
            if not batch:
                break

            # get the waiting runs that belong to these sessions
            session_ids = [s.id for s in batch if s.status == "W"]
            waiting_runs = FlowRun.objects.filter(status="W", session_id__in=session_ids).only(
                "session", "parent_uuid"
            )
            waiting_runs_by_session = {r.session_id: r for r in waiting_runs}

            for session in batch:
                waiting_run = waiting_runs_by_session.get(session.id)
                if waiting_run:
                    session.wait_resume_on_expire = bool(waiting_run.parent_uuid)  # true if run has a parent
                else:
                    session.wait_resume_on_expire = False
                session.save(update_fields=("wait_resume_on_expire",))
                num_updated += 1

            print(f" > updated {num_updated}")


def reverse(apps, schema_editor):
    pass


def apply_manual():  # pragma: no cover
    from django.apps import apps

    populate_wait_resume_on_expire(apps, schema_editor=None)


class Migration(migrations.Migration):

    dependencies = [
        ("flows", "0267_auto_20220106_2036"),
    ]

    operations = [migrations.RunPython(populate_wait_resume_on_expire, reverse)]
