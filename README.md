1. Định dạng các file text nhập vào: 
1.1. item.txt
Dòng đầu tiên chứa số lượng n các mặt hàng
2n dòng tiếp theo: mỗi 2 dòng bao gồm dòng đầu là tên mặt hàng, dòng tiếp theo là đơn vị đo của mặt hàng đó

1.2. node.txt
Dòng đầu tiên: cờ chỉ ra rằng phần tiếp theo là dữ liệu của node dạng nào, bao gồm 'market', 'vendor', 'depot'
Dòng tiếp theo chứa số lượng n các điểm giao hàng
2n dòng tiếp theo: mỗi 2 dòng bao gồm 1 dòng là tọa độ của điểm, dòng tiếp theo là yêu cầu cung cấp đối với từng loại mặt hàng (cần update để input vào theo dạng pair)
Dòng tiếp theo (nếu có): là cờ chỉ ra dạng của node của phần tiếp theo, tương tự như trên

1.3. vehicle.txt
Dòng đầu tiên: số lượng các xe là n
n dòng tiếp theo: dòng thứ i+1 là sức chứa tối đa của xe thứ i đối với từng loại mặt hàng (cần update thành dạng pair)

1.4. route_mass.txt
Bảng chứa độ dài quãng đường đi giữa các điểm

1.5. ...json
Lưu các node dưới cấu trúc dict 
JSON:
    'length': length
    'market': {
        number: {
            'location': {
                'lat': x
                'long': y
            }
            'demand_list':{
                number: {
                    'id': id
                    'demand': demand
                }
            }
        }
    }

2. Định dạng các file output:
2.1. phase2.json
Output của phase 2: clustering các market thành các cluster, lưu dưới dạng file json với cấu trúc: 
{
    cluster_id: {
        'id':id
        'center': {
            'lat':x
            'long':y
        }
        node_list:{
            node_id:{
                'id':id
                'demand':{
                    'item'i:demand
                }
            }
        }
    }
}