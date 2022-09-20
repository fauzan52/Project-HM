{
    'name': 'Module Custom Pembelian',
    'version': '13.0.1.0.8',
    'category': 'purchase',
    'summary': 'Module Custom Pembelian',
    'description': """
        Ini adalah module custom Fauzan Alghifari
    """,
    'website': '',
    'author': 'Fauzan Alghifari',
    'depends': ['web', 'base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/algoritma_pembelian_view.xml',
        'views/algoritma_pembelian_action.xml',
        'views/algoritma_pembelian_menuitem.xml',
        'views/algoritma_pembelian_sequence.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'OEEL-1',
}
