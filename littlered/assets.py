PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'littlered/js/navbar.js',
        ),
        'output_filename': 'littlered-min/js/base.js',
    }
}

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'littlered/css/main.scss',
            'littlered/css/fonts/css/*.css'
        ),
        'output_filename': 'littlered-min/css/base.css',
        'extra_context': {
            'media': 'all',
        },
    },
}
