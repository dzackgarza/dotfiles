import React, { useState, useEffect } from 'react';

interface Props {
  name: string;
  age?: number;
  onUpdate: (data: UserData) => void;
}

type UserData = {
  id: number;
  name: string;
  email: string;
};

const UserComponent: React.FC<Props> = ({ name, age = 18, onUpdate }) => {
  const [count, setCount] = useState<number>(0);
  const [user, setUser] = useState<UserData | null>(null);

  useEffect(() => {
    // Fetch user data
    fetchUser(name).then(setUser);
  }, [name]);

  const handleClick = async (): Promise<void> => {
    const data = await updateUser({ ...user!, count });
    onUpdate(data);
  };

  return (
    <div className="user-component">
      <h1>Hello {name}!</h1>
      {age && <p>Age: {age}</p>}
      <button onClick={() => setCount(c => c + 1)}>
        Count: {count}
      </button>
    </div>
  );
};

export default UserComponent;