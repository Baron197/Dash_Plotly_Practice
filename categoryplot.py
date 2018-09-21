import plotly.graph_objs as go
import seaborn as sns

dfTips = sns.load_dataset('tips')

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
}
def getPlot(jenis, xCategory) :
    return [listGOFunc[jenis](
                x=dfTips[xCategory],
                y=dfTips['tip'],
                text=dfTips['day'],
                opacity=0.7,
                name='Tip',
                marker=dict(color='blue'),
                legendgroup='Tip'
            ),
            listGOFunc[jenis](
                x=dfTips[xCategory],
                y=dfTips['total_bill'],
                text=dfTips['day'],
                opacity=0.7,
                name='Total Bill',
                marker=dict(color='orange'),
                legendgroup='TotalBill'
            )]