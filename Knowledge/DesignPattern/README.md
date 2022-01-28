# Design Pattern

## Creational Patterns

### *"객체를 생성할 때"*

| Pattern name | When used |
| --- | --- |
| [Abstract Factory](.\Creational\abstract_factory.ipynb) | *객체군이 병렬적*이라서 단일 객체군 선택을 쉽게 할 수는 없을까? |
| [Factory Method](.\Creational\factory_method.ipynb) | 슈퍼 클래스에 *객체를 생성하는 인터페이스를 제공하고 서브 클래스에서 생성될 객체의 유형을 변경할 수 있도록* 할 수는 없을까? |
| [Builder](.\Creational\builder.ipynb) | (생성자 오버라이딩 개념이 있는 프로그래밍 언어의 경우) *생성자에 전달할 인수가 복잡*할 때 어쩌지? |
| [Prototype](.\Creational\prototype.ipynb) | *기존 객체로부터 객체를* 만들 수는 없을까? |
| [Singleton](.\Creational\singleton.ipynb) | *생성자를 여러번 호출하더라도 한 인스턴스만 반환*하게 할 수는 없을까? |

## Structural Patterns

### *"객체를 설계할 때"*

| Pattern name | When used |
| --- | --- |
| [Adapter](.\Structural\adapter.ipynb) | *B를 A처럼 쓰고 싶은데* 어쩌지? |
| [Britge](.\Structural\bridge.ipynb) | *A와 B 사이에 추상화 단계*를 두면 좋을 것 같은데? |
| [Composite](.\Structural\composite.ipynb) | *트리 형태의 객체 구조에서 모든 노드 또는 리프가 동일한 인터페이스*를 지니게 하려면 어떻게 하지? |
| [Decorator](.\Structural\decorator.ipynb) | 클라이언트가 *객체를 래핑하는 방식으로 객체에 추가적인 동작을 부여*하게 할 수 없을까? |
| [Facade](.\Structural\facade.ipynb) | 복잡한 저수준 코드들의 동작을 *쉬운 인터페이스*로 제공하고 싶은데? |
| [Flyweight](.\Structural\flyweight.ipynb) | *객체가 너무 많아서 메모리 문제*가 있을 줄은 몰랐는걸? |
| [Proxy](.\Structural\proxy.ipynb) | *A가 B에 요청을 위임할 때 사이에 C를 두어*서 C가 추가적인 동작을 수행하도록 구성할 수 있지 않을까? |

## Behavioral Patterns

### *"객체가 이렇게 동작하면 좋을텐데"*

| Pattern name | When used |
| --- | --- |
| [Chain of responsibility](.\Behavioral\chain_of_responsibility.ipynb) | 내가 할 수 있으면 하고, 못 한다면 다음번 녀석한테 넘기고 |
| [Command](.\Behavioral\command.ipynb) | "너 이거 해"가 아닌 "이거 하는 녀석"을 전달하여 활용 |
| [Iterator](.\Behavioral\iterator.ipynb) | 컬렉션의 요소를 순회하는 객체를 제공 |
| [Mediator](.\Behavioral\mediator.ipynb) | 여러 객체들의 의존성을 관제탑처럼 중간에서 중재 |
| [Memento](.\Behavioral\memento.ipynb) | 객체의 변경 내역을 기록하여 복원 기능을 구현 |
| [Observer (Pub-Sub)](.\Behavioral\observer.ipynb) | 어떠한 동작이 발생했다는 사실을 여러 객체에게 전파 |
| [State](.\Behavioral\state.ipynb) | 유한상태기계처럼 조건마다 동일한 요청이 다른 방식으로 처리 |
| [Strategy](.\Behavioral\strategy.ipynb) | 알고리즘을 구현한 객체 중 하나를 선택하여 활용 |
| [Template Method](.\Behavioral\template_method.ipynb) | 알고리즘의 뼈대만 정의된 메서드의 동작을 서브클래스에서 구현 |
| [Visitor](.\Behavioral\visitor.ipynb) | 이미 정의된 객체군의 코드를 건들지 않고도 추가적인 동작을 부여하기가 가능 |