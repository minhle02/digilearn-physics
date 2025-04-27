
## Questions module

### Guide to write questions

To quickly write questions and answer for physics problems, this project aims to use markdown for easy wrting and parsing.

Each markdown file for question has format:

```
# Chương <chapter id> : <chapter name>

## <module id> : <module name>

### Câu hỏi <exercise_id> - <exercise_rating>

#### Answer
```

For easy parsing, the format for wrting questions in markdown is:

`#`: Heading 1 level. This is use to indicate chapter ID and chapter name. This ID should match with Openstax chapter number

`##`: Heading 2 level. Use to indicate module ID and module name. The ID should match with Openstax module number (example: 2.1, 2.2, etc). Chapter name must be follow after a `:`

`###`: Heading 3 level, use to indicate question id and question rating. This must be in format `<exercise_id> - <exercise_rating>`. The letter before `<exercise_id>` does not matters. `<exercis_id>` must be `<module_id>.<number>`. For example: 2.1.1, 2.1.2

There are 3 types of questions:

1. Multiple choices
    - The last 4 lines must be designated to choices. each choice must start with (A), (B), (C), or (D)
    - There must be 4 choices
    - First several lines are for description. You can add as many lines as you want
    - Example:
```
Vi khuẩn di chuyển tới lui bằng cách sử dụng tiên mao (bộ phận tương tự chiếc đuôi nhỏ). Tốc độ quan sát được là $50\mu m/s\ (50 * 10^{-6} m/s)$. Tổng quãng đường đi được của một vi khuẩn rất lớn so với kích thước của nó, trong khi độ dịch chuyển của nó lại nhỏ. Tại sao lại như vậy?

(A) Vì vi khuẩn di chuyển với tốc độ rất cao trong một khoảng thời gian ngắn.

(B) Vì vi khuẩn thường xuyên thay đổi hướng di chuyển, dẫn đến nhiều đoạn đường nhỏ cộng lại thành quãng đường lớn, nhưng vị trí cuối cùng không cách xa vị trí ban đầu.

(C) Vì roi của vi khuẩn có chiều dài lớn hơn nhiều so với kích thước của thân vi khuẩn.

(D) Vì vi khuẩn di chuyển theo đường thẳng ra rất xa.
```

2. Simple short answers
    - You can add any question lines for this type

3. Short answers with sub questions
    - The first few lines are description. Add as much as you want
    - Any subquestion must startswith (`<lowercase letter>`) such as (a), (b), (c), ...
    - Example:
```
Tìm các thông tin sau cho đường đi D trong hình dưới:

**(a)** Quãng đường đã đi

**(b)** Độ lớn của độ dịch chuyển từ điểm đầu đến điểm cuối

**(c)** Độ dịch chuyển từ điểm đầu đến điểm cuối
``` 
`####`: Heading 4 level, use to indicate answer to the nearest question befor it (Heading 3 level)

There are 3 types of answers:

1. Multiple choices
    - Only 1 option in (A), (B), (C), or (D). This must match with the prefix letter for choice in the question section
    - Example:
```
(B)
```

2. Simple short answers
    - You can add any answer lines for this type

3. Short answers with sub questions
    - Each line should start with a (`<lowercase letter>`). This must be match with the sub-question id in the question section.
    - Example:
```
**(a)** 7 m

**(b)** 7 m

**(c)** +7 m
``` 

#### Static data:

Some question may need static data (image, video). It is recommended to use python script to generate static data

Any static data should be in the `static` folder within the same directory as the `.md` file.

You can add markdown style image in the markdown text:

```
![Đồ thị](./static/figure-c2-m1-e1.png)
```

In the `[]` is the description, in the `()` is the image path

### How to parse the questions

Install `uv` for package management:
```
pip install uv
```

Sync environment:
```
uv sync
```

The `Questions/core` package has the tool for parsing data. To parse data, use class MDParser and pass the name of .md file. For example:

```
md_file = "../chapter-02/questions.md"
parser = MDParser(md_file)
modules = parser.get_modules()
```

### TODO:
- [ ] Add parsing units and data in answer