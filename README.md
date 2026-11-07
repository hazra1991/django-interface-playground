# django-admin-playground

small django project i made to try out the django admin with the
[django-admin-interface](https://github.com/fabiocaccamo/django-admin-interface) theme.
it turned into a debugging rabbit hole, so this repo is mostly the setup i used to
reproduce and dig into that.

## what happened

i turned on django logging at DEBUG level (to `debug.log`) and noticed every admin page
was logging stuff like:

```
Exception while resolving variable 'adminform' in template 'admin/index.html'
Exception while resolving variable 'inline_admin_formsets' in template 'admin/index.html'
```

admin-interface's `base_site.html` does `{% if adminform and inline_admin_formsets %}` to
decide about changeform tabs. on pages that are not change forms (index, changelist ...)
those vars are not in the context at all, so django raises `VariableDoesNotExist`
internally, swallows it and logs it. the page works fine, but the log gets noisy.

steps i went through:

- made `testapp` with a dummy `testdb` model so i had something in the admin
- added debug toolbar + file logging to see what the templates were doing
- added prints in `admin_interface_use_changeform_tabs` and a dummy tag to see what is
  actually passed in (`notes/debug-changeform-tabs.patch`, my local debug changes)
- `mycustome.html` + `/my/` view: plain template with `{% if title %}` / `{% if abcdefc %}`
  to check this is normal django behaviour for missing vars and not something theme specific

## the fix i tried

added a `admin_interface_resolve_variable` simple tag that looks the var up in
`context.flatten()` and returns a default instead of raising, and used it in
`base_site.html` for `adminform` / `inline_admin_formsets`. with tests.

- branch: https://github.com/hazra1991/django-admin-interface/tree/fix/missing-context-vars
- PR: https://github.com/fabiocaccamo/django-admin-interface/pull/453

the PR got closed, as per the maintainer it's not an actual issue in the package. fair
enough, but i learned a lot about how django resolves template variables and context on
the way.

## other stuff

- `experiments/thread_local.py` - side experiment with `threading.local()`, was reading
  about how per-request/thread state works

## run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cd mytestproject
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

then open http://127.0.0.1:8000/admin/ and check `mytestproject/debug.log`.

note: `SECRET_KEY` in settings is the default dev key from startproject, its only for
local use.
