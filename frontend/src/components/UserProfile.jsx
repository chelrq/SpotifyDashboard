import './UserProfile.css'

function UserProfile({ user }) {
  return (
    <div className="user-profile">
      {user.image && (
        <img
          src={user.image}
          alt={user.name}
          className="user-avatar"
        />
      )}
      <div className="user-info">
        <div className="user-name">{user.name}</div>
        <div className="user-stats">
          <span className="stat">
            <span className="stat-value">{user.followers.toLocaleString()}</span>
            <span className="stat-label">Followers</span>
          </span>
        </div>
      </div>
    </div>
  )
}

export default UserProfile
