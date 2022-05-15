from dash import dash_table


class DataTableEnhanced(dash_table.DataTable):

    def __init__(self, _id, data, columns, tooltip_data):
        super(DataTableEnhanced, self).__init__(id=_id,
                                                data=data,
                                                columns=columns,
                                                page_size=9,
                                                fixed_columns={'headers': True, 'data': 1},
                                                sort_action='native',
                                                tooltip_data=tooltip_data,
                                                tooltip_duration=None,
                                                style_table={'minWidth': '100%'},
                                                style_cell={'overflow': 'hidden',
                                                            'minWidth': '9.25rem', 'width': '9.25rem',
                                                            'maxWidth': '9.25rem',
                                                            'textOverflow': 'ellipsis',
                                                            'textAlign': 'right',
                                                            },
                                                style_cell_conditional=[{'if': {'column_id': 'name'},
                                                                         'textAlign': 'left',
                                                                         'minWidth': '11.25rem',
                                                                         'width': '11.25rem',
                                                                         'maxWidth': '11.25rem'}]
                                                )
