# [[2.1 Độ dịch chuyển]]

- Động học là cách mô tả chuyển động trong khi bỏ qua nguyên nhân gây ra chuyển động. Trong chương này, chúng ta chỉ nghiên cứu chuyển động trên một đường thẳng, gọi là chuyển động một chiều.
- Độ dịch chuyển là sự thay đổi về vị trí của một vật.
- Gọi $\Delta x$ là độ dịch chuyển, ta có:
$$
\Delta x = x_s - x_đ
$$
Trong đó, $x_đ$ là vị trí ban đầu của vật, $x_s$ là vị trí cuối cùng của vật. Trong công thức này, chữ cái La Mã $\Delta$ (delta) luôn chỉ đến "sự thay đổi" của bất kỳ đại lượng nào phía sau nó. Đơn vị SI cho độ dịch chuyển là mét (m). Độ dịch chuyển có hướng và có độ lớn.
+ Khi làm bài tập nào, hãy chọn một hướng làm chiều dương.
+ Khoảng cách (quãng đường) là độ lớn của độ dịch chuyển giữa hai điểm.
+ Quãng đường đi được là tổng chiều dài các đoạn đường đã đi qua giữa 2 điểm.
# [[2.2 Đại lượng vector, Đại lượng vô hướng, và Hệ quy chiếu]]
+ Vector là đại lượng có hướng và độ lớn.
+ Đại lượng vô hướng là đại lượng chỉ có độ lớn, không có hướng.
+ Độ dịch chuyển và vận tốc là các đại lượng vector, còn khoảng cách và tốc độ là đại lượng vô hướng.
+ Trong chuyển động một chiều, hướng được đánh dầu bằng dấu cộng (+) hoặc dấu (-) để phân biệt phải hay trái, hoặc trên hay dưới.
# [[2.3 Thời gian, Vận tốc, và Tốc độ]]
+ Đơn vị SI của thời gian là giây (s). Khoảng thời gian trôi qua của một sự kiện là
$$
\Delta t = t_s - t_0
$$

Trong đó, $t_s$ là mốc thời gian kết thúc, còn $t_đ$ là mốc thời gian ban đầu. Mốc thời gian ban đầu thường được chọn là 0, khi đó khoảng thời gian trôi qua chỉ là $t$.
+ Vận tốc trung bình $\overline v$ là độ dịch chuyển chia cho thời gian đi được:
$$
\overline v = \frac {\Delta x}{\Delta t} = \frac {x_s - x_0}{t_s - t_0}
$$
+ Đơn vị SI của vận tốc là m/s.
+ Vận tốc là đại lượng vector, nên vận tốc có hướng.
+ Vận tốc tức thời $v$ là vận tốc tại một khoảnh khắc hoặc là vận tộc trung bình trong một khoảng thời gian rất nhỏ.
+ Tốc độ tức thời là độ lớn của vận tóc tức thời.
+ Tốc độ tức thời là đại lượng vô hướng.
+ Tốc độ trung bình bằng tổng khoảng cách chia cho tổng thời gian đi được. (Tốc độ trung bình **không phải** là vân tốc trung bình). 
+ Tốc độ là đại lượng vô hướng.
# [[2.4 Gia tốc]]
+ Gia tốc là tốc độ thay đổi của vận tốc. **Gia tốc trung bình** $a$ là:
$$
\overline a = \frac {\Delta v}{\Delta t} = \frac {v_s - v_0} {t_s - t_0} 
$$
+ Đơn vị của gia tốc là $m/s^2$ .
+ Gia tốc là đại lượng vector, nên gia tốc vừa có hướng vừa có độ lớn.
+ Sự thay đổi về độ lớn hoặc hướng của vận tốc tạo ra gia tốc.
+ Gia tốc tức thời $a$ là gia tốc tại một thời điểm.
+ Giảm tốc là gia tốc có hướng ngược lại với hướng của vận tốc.
# [[2.5 Phương trình Chuyển động một chiều với gia tốc không đổi]]
+ Để đơn giản hoá việc tính toán, chọn gia tốc không đổi, nghĩa là $\overline a = a$ tại bất kỳ thời điểm nào.
+ Chọn mốc thời gian ban đầu là 0.
+ Vị trí ban đầu và vận tốc ban đầu đều được ký hiệu số 0 ở dưới, còn vị trí và vận tốc ban đầu **không** có số 0 ở dưới. 
$$
\Delta t = t
$$
$$
\Delta x = x - x_0
$$
$$
\Delta v = v_0 - v
$$
+ Các phương trình chuyển động một chiều với gia tốc không đổi $a$:
$$
x = x_0 + \overline v t
$$
$$
\overline v = \frac{v_0 + v} {2}
$$
$$
v = v_0 + at
$$
$$
x = x_0 + v_0 t + \frac {1}{2}a t^2
$$$$
v^2 = v_0 ^ 2 + 2 a x - x_0
$$
+ Trong chuyển động thẳng đứng, thay $x$ bằng $y$ .
# [[2.6 Phương pháp giải các bài toán chuyển động trên đường thẳng]]
+ 6 bước cơ bản để giải bài tập:
	1. Đọc và hiểu kỹ đề bài, xác định nguyên lý vật lý nào xuất hiện.
	2. Ghi lại các dữ kiện đã cho, hoặc các dữ kiện suy ra được từ đề bài (xác định dữ kiện).
	3. Xác định đề bài muốn tìm gì (xác định ẩn số).
	4. Tìm các phương trình có thể giúp giải quyết bài toán.
	5. Thay các dữ kiện đã biết cùng với đơn vị vào phương trình, và giải các phương trình để tìm ra đáp án.
	6. Kiểm tra lại xem đáp án có hợp lý không.
# [[2.7 Rơi tự do]]
+ Bỏ qua lực cản không khí, một vật rơi tự do với gia tốc không đổi.
+ Trên trái đất, tất cả mọi vật đều chịu gia tốc trọng trường (gia tốc gây ra bởi trọng lực) với độ lớn trung bình:
$$
g = 9.80\ m / s^2
$$
+ Sử dụng gia tốc $+g$ hay $-g$ tuỳ thuộc vào cách chọn hệ quy chiếu. Nếu chọn hệ quy chiếu hướng lên, $a = -g = -9.80\ m/s^2$. Nếu chọn hệ quy chiếu hướng xuống, $a = +g = 9.80 m/s^2$ . Vì gia tốc này không đổi, nên cách phương trình động học có thể được áp dụng với $a=-g$ hoặc $a=+g$.